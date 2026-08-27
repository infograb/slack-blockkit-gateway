#!/usr/bin/env python3
"""Block Kit 페이로드 로컬 검증기 — 게시 전 한계 위반을 잡는다.

기준: 2026-08-24 InfoGrab 실측(T01~T42) + docs.slack.dev.
실측으로 확인된 거부 조건은 ERROR, 문서 기준은 ERROR, 위험 조합은 WARN.

사용: python3 validate_payload.py <payload.json> [더.json ...]
  payload 형식: chat.postMessage 인자({ "text": ..., "blocks": [...] }) 또는 blocks 배열 단독.
종료 코드: ERROR가 하나라도 있으면 1, WARN만 있으면 0, 통과 0.
"""
import json, sys

E, W, I = [], [], []  # errors, warnings, infos

def err(m): E.append(m)
def warn(m): W.append(m)
def info(m): I.append(m)

def tlen(o):
    return len(o.get("text", "")) if isinstance(o, dict) else 0

def check_text_object(o, where, allow_mrkdwn=True):
    if not isinstance(o, dict):
        err(f"{where}: text object가 아님 (문자열이어야 하는 곳에 객체, 또는 반대)")
        return
    if o.get("type") not in ("plain_text", "mrkdwn"):
        err(f"{where}: text object type은 plain_text|mrkdwn (got {o.get('type')!r})")
    if tlen(o) < 1:
        err(f"{where}: text는 1자 이상")
    if tlen(o) > 3000:
        err(f"{where}: text {tlen(o)}자 > 3000 [실측 T16]")
    if not allow_mrkdwn and o.get("type") == "mrkdwn":
        err(f"{where}: 여기는 plain_text만 허용")

def check_confirm(c, where):
    if not isinstance(c, dict): return
    if tlen(c.get("title")) > 100: err(f"{where}.confirm.title > 100")
    if tlen(c.get("text")) > 300: err(f"{where}.confirm.text > 300")
    if tlen(c.get("confirm")) > 30: err(f"{where}.confirm.confirm > 30")
    if tlen(c.get("deny")) > 30: err(f"{where}.confirm.deny > 30")

def check_option(o, where, url_allowed=False):
    if tlen(o.get("text")) > 75: err(f"{where}: option text {tlen(o.get('text'))}자 > 75")
    v = o.get("value", "")
    if len(str(v)) > 150: err(f"{where}: option value > 150")
    if tlen(o.get("description")) > 75: err(f"{where}: option description > 75")
    if "url" in o and not url_allowed:
        err(f"{where}: option.url은 overflow 전용")
    if isinstance(o.get("text"), dict) and o["text"].get("type") == "mrkdwn" and "select" in where:
        err(f"{where}: select 계열 option은 plain_text만 (radio/checkboxes는 mrkdwn 가능)")

def check_element(el, where, in_actions=False):
    t = el.get("type")
    ph = el.get("placeholder")
    if ph and tlen(ph) > 150: err(f"{where}.placeholder > 150")
    if len(str(el.get("action_id", ""))) > 255: err(f"{where}.action_id > 255")

    if t == "button":
        txt = el.get("text", {})
        if tlen(txt) > 75: err(f"{where}: button text {tlen(txt)}자 > 75 [실측 T24]")
        if len(str(el.get("value", ""))) > 2000: err(f"{where}: button value > 2000")
        if len(str(el.get("url", ""))) > 3000: err(f"{where}: button url > 3000")
        if el.get("style") not in (None, "primary", "danger"): err(f"{where}: button style은 primary|danger")
        check_confirm(el.get("confirm"), where)
    elif t == "overflow":
        opts = el.get("options", [])
        if len(opts) > 5: err(f"{where}: overflow options {len(opts)}개 > 5 [실측 T21]")
        if len(opts) < 1: err(f"{where}: overflow options 없음")
        for i, o in enumerate(opts): check_option(o, f"{where}.options[{i}]", url_allowed=True)
    elif t in ("static_select", "external_select", "users_select", "conversations_select", "channels_select"):
        opts, groups = el.get("options"), el.get("option_groups")
        if opts and groups: err(f"{where}: options과 option_groups 동시 사용 불가")
        if opts and len(opts) > 100: err(f"{where}: select options > 100")
        if groups and len(groups) > 100: err(f"{where}: option_groups > 100")
        for i, o in enumerate(opts or []): check_option(o, f"{where}({t}).options[{i}]")
    elif t and t.startswith("multi_"):
        if in_actions:
            err(f"{where}: {t} in actions — 유저 토큰 실측 거부(unsupported element: multiselect) [실측 T08/T08c]. section accessory로 이동할 것")
        for i, o in enumerate(el.get("options", [])[:101]): check_option(o, f"{where}.options[{i}]")
        if len(el.get("options", [])) > 100: err(f"{where}: multi options > 100")
    elif t == "radio_buttons":
        if len(el.get("options", [])) > 10: err(f"{where}: radio options > 10")
    elif t == "checkboxes":
        if len(el.get("options", [])) > 10: err(f"{where}: checkboxes options > 10")
        inits = el.get("initial_options", [])
        if inits and {json.dumps(x, sort_keys=True) for x in inits} - {json.dumps(x, sort_keys=True) for x in el.get("options", [])}:
            err(f"{where}: initial_options은 options과 정확히 일치해야 함")
    elif t == "feedback_buttons":
        for k in ("positive_button", "negative_button"):
            b = el.get(k, {})
            if not b.get("value"): err(f"{where}.{k}: value 필수")
            if tlen(b.get("text")) > 75: err(f"{where}.{k}.text > 75")
    elif t == "icon_button":
        if el.get("icon") != "trash": err(f"{where}: icon_button icon은 현재 trash만 지원")
        if not el.get("text"): err(f"{where}: icon_button은 text 필수 [실측 T38]")
    elif t == "workflow_button":
        if not el.get("workflow"): err(f"{where}: workflow_button은 workflow(trigger) 필수")
    elif t == "image":
        if len(str(el.get("image_url", ""))) > 3000: err(f"{where}: image_url > 3000")
        if not el.get("alt_text"): err(f"{where}: image element alt_text 필수")
    elif t in ("datepicker", "timepicker", "datetimepicker"):
        pass
    elif t in ("plain_text_input", "rich_text_input", "email_text_input", "url_text_input", "number_input", "file_input"):
        if t == "rich_text_input": warn(f"{where}: rich_text_input은 Messages 불가(Modals/Home)")
        if t in ("email_text_input", "url_text_input", "number_input", "file_input"):
            warn(f"{where}: {t}는 Modals 전용 — 메시지 게시 시 실패 가능")
    elif t == "url":
        pass
    else:
        warn(f"{where}: 알 수 없는 element type {t!r} — 레퍼런스 확인")

def check_block(b, i, md_total):
    where = f"blocks[{i}]"
    t = b.get("type")
    if len(str(b.get("block_id", ""))) > 255: err(f"{where}.block_id > 255")

    if t == "section":
        txt = b.get("text")
        if txt is None and not b.get("fields") and not b.get("accessory"):
            err(f"{where}: section은 text|fields|accessory 중 하나 필요")
        if txt:
            check_text_object(txt, where + ".text")
            if "**" in txt.get("text", "") and txt.get("type") == "mrkdwn":
                warn(f"{where}.text: '**' 포함 — mrkdwn에서 **는 리터럴로 보일 수 있음. 볼드는 *한 겹*. CommonMark 의도라면 markdown 블록 사용")
        flds = b.get("fields", [])
        if len(flds) > 10: err(f"{where}: fields {len(flds)}개 > 10")
        for j, f in enumerate(flds):
            if tlen(f) > 2000: err(f"{where}.fields[{j}] > 2000")
        acc = b.get("accessory")
        if acc: check_element(acc, where + ".accessory")
    elif t == "header":
        check_text_object(b.get("text", {}), where + ".text", allow_mrkdwn=False)
        if tlen(b.get("text")) > 150: err(f"{where}: header {tlen(b.get('text'))}자 > 150 [실측 T18]")
    elif t == "context":
        els = b.get("elements", [])
        if len(els) > 10: err(f"{where}: context elements > 10")
    elif t == "context_actions":
        els = b.get("elements", [])
        if len(els) > 5: err(f"{where}: context_actions elements > 5")
        for j, el in enumerate(els):
            if el.get("type") not in ("feedback_buttons", "icon_button"):
                err(f"{where}.elements[{j}]: context_actions에는 feedback_buttons/icon_button만")
            check_element(el, f"{where}.elements[{j}]")
    elif t == "actions":
        els = b.get("elements", [])
        if len(els) > 25: err(f"{where}: actions elements {len(els)}개 > 25")
        for j, el in enumerate(els): check_element(el, f"{where}.elements[{j}]", in_actions=True)
    elif t == "container":
        if tlen(b.get("title")) > 150: err(f"{where}: container title > 150")
        ch = b.get("child_blocks", [])
        if len(ch) > 10: err(f"{where}: child_blocks {len(ch)}개 > 10")
        if b.get("is_collapsible") and not isinstance(b.get("is_collapsible"), bool):
            err(f"{where}: is_collapsible은 boolean")
        for k, cb in enumerate(ch): check_block(cb, f"{i}.child_blocks[{k}]", md_total)
    elif t == "table":
        rows = b.get("rows", [])
        if len(rows) > 100: err(f"{where}: rows {len(rows)} > 100")
        total = 0
        for r, row in enumerate(rows):
            if len(row) > 20: err(f"{where}.rows[{r}]: cells {len(row)} > 20")
            for cell in row:
                if cell.get("type") == "raw_text": total += len(cell.get("text", ""))
                elif cell.get("type") == "raw_number": total += len(str(cell.get("value", cell.get("text", ""))))
                elif cell.get("type") == "rich_text": total += len(json.dumps(cell, ensure_ascii=False))
                else: err(f"{where}.rows[{r}]: 알 수 없는 cell type {cell.get('type')!r}")
        if total > 10000: err(f"{where}: 셀 합산 {total}자 > 10,000")
    elif t == "data_table":
        if not b.get("caption"): err(f"{where}: data_table은 caption 필수")
        rows = b.get("rows", [])
        if not (2 <= len(rows) <= 201): err(f"{where}: rows {len(rows)} — 2~201 범위")
        if b.get("page_size", 5) > 100: err(f"{where}: page_size > 100")
        total = 0
        for r, row in enumerate(rows):
            if len(row) > 20: err(f"{where}.rows[{r}]: cells > 20")
            for cell in row:
                ct = cell.get("type")
                if ct == "raw_number":
                    err(f"{where}.rows[{r}]: raw_number 셀은 유저 토큰 실측 거부 [실측 T40b/c] — raw_text로")
                elif ct == "raw_text": total += len(cell.get("text", ""))
                elif ct == "rich_text": total += len(json.dumps(cell, ensure_ascii=False))
        if total > 20000: err(f"{where}: 셀 합산 > 20,000")
    elif t == "data_visualization":
        if len(str(b.get("title", ""))) > 50: err(f"{where}: title > 50")
        chart = b.get("chart", {})
        segs = chart.get("segments", [])
        if chart.get("type") == "pie":
            if not (1 <= len(segs) <= 12): err(f"{where}: pie segments 1~12")
            for s in segs:
                if not s.get("value", 0) > 0: err(f"{where}: pie value는 0 초과")
                if len(str(s.get("label", ""))) > 20: err(f"{where}: pie label > 20")
        elif chart.get("type") in ("bar", "line", "area", None):
            if chart.get("type") is None: err(f"{where}: chart.type 없음")
            else: info(f"{where}: {chart['type']} 차트 스키마는 미실측 [gaps A8] — pie만 실측됨")
    elif t == "plan":
        if not isinstance(b.get("title"), str): err(f"{where}: plan title은 문자열 [실측 T35]")
        tasks = b.get("tasks", [])
        if len(tasks) > 50: err(f"{where}: plan tasks > 50")
        ids = set()
        for k, task in enumerate(tasks):
            if not isinstance(task.get("title"), str): err(f"{where}.tasks[{k}]: title은 문자열 [실측 T35]")
            if task.get("task_id") in ids: err(f"{where}.tasks[{k}]: task_id 중복")
            ids.add(task.get("task_id"))
    elif t == "task_card":
        if not isinstance(b.get("title"), str): err(f"{where}: task_card title은 문자열 [실측 T36]")
        if b.get("status") not in ("in_progress", "complete", "error", None):
            err(f"{where}: status는 in_progress|complete|error")
    elif t == "markdown":
        md_total[0] += len(b.get("text", ""))
        if b.get("block_id"): info(f"{where}: markdown 블록의 block_id는 무시됨")
        if "<http" in b.get("text", "") and "|" in b.get("text", ""):
            info(f"{where}: <url|text>는 mrkdwn 문법 — markdown 블록에서는 [text](url)")
    elif t == "image":
        if len(str(b.get("image_url", ""))) > 3000: err(f"{where}: image_url > 3000")
        alt = b.get("alt_text")
        if not alt: err(f"{where}: alt_text 필수")
        elif len(alt) > 2000: err(f"{where}: alt_text > 2000")
        if not b.get("slack_file"):
            warn(f"{where}: 외부 image_url은 로드 실패 가능 [실측 T04] — 파일 업로드(slack_file) 권장")
    elif t == "input":
        if tlen(b.get("label")) > 2000: err(f"{where}: label > 2000")
        el = b.get("element", {})
        if el: check_element(el, where + ".element")
        if b.get("dispatch_action") and el.get("type") == "file_input":
            err(f"{where}: dispatch_action과 file_input 병용 불가")
    elif t == "divider":
        pass
    elif t == "file":
        err(f"{where}: file 블록은 직접 게시 불가(조회 전용) — 파일은 업로드 API로")
    elif t == "video":
        warn(f"{where}: video는 links.embed:write + unfurl 도메인 등록 필요 [실측 T15 거부]")
    elif t == "alert":
        warn(f"{where}: alert는 Modals 전용 — 메시지 게시 불가")
    elif t == "card":
        if tlen(b.get("title")) > 150: err(f"{where}: card title > 150")
        if tlen(b.get("body")) > 200: err(f"{where}: card body > 200")
        if len(b.get("actions", [])) > 3: err(f"{where}: card actions > 3")
    elif t == "carousel":
        cards = b.get("cards", b.get("child_blocks", []))
        if cards and not (1 <= len(cards) <= 10): err(f"{where}: carousel 카드 1~10")
    elif t == "rich_text":
        pass
    else:
        warn(f"{where}: 알 수 없는 block type {t!r}")

def validate(payload):
    if isinstance(payload, list):
        payload = {"blocks": payload}
    if not isinstance(payload, dict):
        err("payload는 객체(chat.postMessage 인자) 또는 blocks 배열이어야 함"); return
    # 2단계 파일(initial/final 서브객체)은 각각 검증
    if isinstance(payload.get("initial"), dict) or isinstance(payload.get("final"), dict):
        for phase in ("initial", "final"):
            sub = payload.get(phase)
            if isinstance(sub, dict):
                info(f"-- phase: {phase}")
                validate(sub)
        return
    blocks = payload.get("blocks")
    if not payload.get("text"):
        warn("top-level text(폴 스트링) 없음 — 알림/검색/스크린리더에서 내용이 비고, blocks 실패 시 진단이 어려움 [실측 규칙]")
    if blocks is None:
        info("blocks 없음 — 평문 메시지"); return
    if len(blocks) > 50:
        err(f"blocks {len(blocks)}개 > 50 [실측 T17]")
    md_total = [0]
    for i, b in enumerate(blocks):
        check_block(b, i, md_total)
    if md_total[0] > 12000:
        err(f"markdown 블록 합산 {md_total[0]}자 > 12,000")

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    any_err = False
    for path in sys.argv[1:]:
        E.clear(); W.clear(); I.clear()
        try:
            payload = json.load(open(path))
        except Exception as e:
            print(f"✗ {path}: JSON 파싱 실패 — {e}"); any_err = True; continue
        validate(payload)
        for m in E: print(f"  ERROR {m}")
        for m in W: print(f"  WARN  {m}")
        for m in I: print(f"  info  {m}")
        print(f"{'✗' if E else '✓'} {path}: error {len(E)}, warn {len(W)}")
        any_err = any_err or bool(E)
    sys.exit(1 if any_err else 0)

if __name__ == "__main__":
    main()
