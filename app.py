    # Nesting (basit yerleştirme)
    doc = ezdxf.new()
    msp = doc.modelspace()
    x, y, max_y = 0, 0, 0
    plaka_w, plaka_h = 2100, 2800
    padding = 10

    for p in paneller:
        file = f"{klasor}/{p['isim']}.dxf"
        if not os.path.exists(file):
            continue

        panel_doc = ezdxf.readfile(file)
        panel_msp = panel_doc.modelspace()
        w, h = p["w"], p["h"]

        if x + w > plaka_w:
            x = 0
            y += max_y + padding
            max_y = 0
        if y + h > plaka_h:
            st.warning(f"{p['isim']} plakaya sığmadı, atlandı.")
            continue

        for e in panel_msp:
            try:
                e_copy = e.copy()
                e_copy.translate(dx=x, dy=y)
                msp.add_entity(e_copy)
            except Exception as err:
                st.warning(f"{p['isim']} parçasında eleman atlandı: {e.dxftype()} ({str(err)})")

        x += w + padding
        if h > max_y:
            max_y = h

    doc.saveas("yerlesim.dxf")
