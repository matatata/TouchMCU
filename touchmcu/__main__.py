import subprocess
import sys
import getopt

from touchmcu.master import create_assignment, create_fader_banks, create_master_fader, create_timecode
from touchmcu.touchosc import Rect
from touchmcu.touchosc.controls import Pager, Page
from touchmcu.touchosc.document import Document
from touchmcu.touchosc.midi import MidiNotes

from touchmcu import load_all_scripts, load_overlay
from touchmcu.track import create_track
from touchmcu.transport import create_automation, create_function_select, create_global_view, create_jog, create_modifiers, create_transport, create_transport_assignment, create_transport_timecode, create_utilities


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ho:s",["help","overlay=","show"])
    except getopt.GetoptError:
        print('python -m touchmcu -o <overlay_name>')
        sys.exit(2)

    show = False
    overlay_name = "default"

    for opt, arg in opts:
        if opt == '-h':
            print('python -m touchmcu -o <overlay_name>')
            sys.exit()
        elif opt in ("-o", "--overlay"):
            overlay_name = arg
        elif opt in ("-s", "--show"):
            show = True

    # ====== OVERLAY ===============================================================

    overlay = load_overlay(f"{overlay_name}.yml")

    # ====== DOCUMENT ==============================================================

    doc = Document(1024, 768)

    doc.root["script"] = load_all_scripts(
        "table_utils.lua",
        "lcd.lua"
    )

    pager = Pager(
        parent=doc.root,
        name="pager",
        frame=doc.root["frame"]
    )

    # ====== TRACKS ================================================================

    track_page = Page(
        parent=pager,
        name="track_page",
        tabLabel="Tracks",
        frame=Rect(
            x=0,
            y=pager["tabbarSize"],
            w=pager["frame"]["w"],
            h=pager["frame"]["h"] - pager["tabbarSize"]
        )
    )

    for i in range(8):
        tr = create_track(track_page, overlay, i)
        tr["frame"].move(2+102*i, 0)

    timecode = create_timecode(track_page, overlay)
    timecode["frame"].move(820, 0)

    assign = create_assignment(track_page, overlay)
    assign["frame"].move(820, 106)

    banks = create_fader_banks(track_page, overlay)
    banks["frame"].move(820, 342)

    master = create_master_fader(track_page)
    master["frame"].move(922, 342)

    # ====== TRANSPORT =============================================================

    transport_page = Page(
        parent=pager,
        name="transport_page",
        tabLabel="Transport",
        frame=Rect(
            x=0,
            y=pager["tabbarSize"],
            w=pager["frame"]["w"],
            h=pager["frame"]["h"] - pager["tabbarSize"]
        )
    )

    global_view = create_global_view(transport_page, overlay)
    global_view["frame"].move(2, 2)

    functions = create_function_select(transport_page, overlay)
    functions["frame"].move(2, 122)

    modifiers = create_modifiers(transport_page, overlay)
    modifiers["frame"].move(2, 242)

    automation = create_automation(transport_page, overlay)
    automation["frame"].move(202, 242)

    utilities = create_utilities(transport_page, overlay)
    utilities["frame"].move(482, 242)

    transport = create_transport(transport_page, overlay)
    transport["frame"].move(2, 422)

    timcode = create_transport_timecode(transport_page, overlay)
    timcode["frame"].move(678, 2)

    assign = create_transport_assignment(transport_page, overlay)
    assign["frame"].move(678, 122)

    jog = create_jog(transport_page, overlay)
    jog["frame"].move(678, 242)


    # ==============================================================================

    fn = f"./{overlay['overlay_title']}.tosc"

    doc.finalise()
    doc.save(fn)

    if show:
        subprocess.call(["open", fn])

if __name__ == "__main__":
    main(sys.argv[1:])