import ezdxf

PLAKA_GENISLIK = 2440
PLAKA_YUKSEKLIK = 1220
ARA_BOSLUK = 10
CABINEO_CAPI = 15
CABINEO_MARGIN = 64
CABINEO_SPACING = 128

parcalar = [
    (600, 400),  # Parça 1
    (400, 400),  # Parça 2
    (300, 600),  # Parça 3
    (500, 300)   # Parça 4
]

def add_cabineo_holes(msp, x0, y0, gen, yuk):
    # Sadece uzun kenarlara Cabineo deliği yerleştir (soldan sağa)
    x_positions = list(range(CABINEO_MARGIN, int(gen - CABINEO_MARGIN) + 1, CABINEO_SPACING))
    y_center = y0 + yuk / 2

    for x in x_positions:
        msp.add_circle(center=(x0 + x, y_center), radius=CABINEO_CAPI / 2, dxfattribs={'layer': 'cabineo'})

def nesting_with_cabineo(parcalar, plaka_genislik, plaka_yukseklik, bosluk, filename="nesting_cabineo.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Plaka çizimi
    msp.add_lwpolyline([
        (0, 0),
        (plaka_genislik, 0),
        (plaka_genislik, plaka_yukseklik),
        (0, plaka_yukseklik),
        (0, 0)
    ], dxfattribs={'layer': 'plaka'})

    x = y = 0
    max_satir_yukseklik = 0

    for idx, (gen, yuk) in enumerate(parcalar):
        if x + gen > plaka_genislik:
            x = 0
            y += max_satir_yukseklik + bosluk
            max_satir_yukseklik = 0

        if y + yuk > plaka_yukseklik:
            print(f"Parça sığmadı: {idx+1}. parça ({gen}x{yuk})")
            continue

        # Parça çerçevesi
        msp.add_lwpolyline([
            (x, y),
            (x + gen, y),
            (x + gen, y + yuk),
            (x, y + yuk),
            (x, y)
        ], dxfattribs={'layer': 'parca'})

        # Parça etiketi
        msp.add_text(f"P{idx+1}", dxfattribs={'height': 10}).set_pos((x + 5, y + 5))

        # Cabineo delikleri
        add_cabineo_holes(msp, x, y, gen, yuk)

        x += gen + bosluk
        max_satir_yukseklik = max(max_satir_yukseklik, yuk)

    doc.saveas(filename)
    print(f"DXF kaydedildi: {filename}")

nesting_with_cabineo(parcalar, PLAKA_GENISLIK, PLAKA_YUKSEKLIK, ARA_BOSLUK)
