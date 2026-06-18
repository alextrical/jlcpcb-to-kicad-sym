def resistor_packages():
    return [
        ('0402', 'Resistor_SMD:R_0402_1005Metric', 'like "%402"'),
        ('0603', 'Resistor_SMD:R_0603_1608Metric', 'like "%603"'),
        ('0805', 'Resistor_SMD:R_0805_2012Metric', 'like "%805"'),
        ('1206', 'Resistor_SMD:R_1206_3216Metric', 'like "%1206"'),
    ]

def diode_packages():
    return [
        ('0402', 'Diode_SMD:D_0402_1005Metric', 'like "%402"'),
        ('0603', 'Diode_SMD:D_0603_1608Metric', 'like "%603"'),
        ('0805', 'Diode_SMD:D_0805_2012Metric', 'like "%805"'),
        ('1206', 'Diode_SMD:D_1206_3216Metric', 'like "%1206"'),
        ('SOD-323', 'Diode_SMD:D_SOD-323', '= "SOD-323"'),
        ('SMA(DO-214AC)', 'Diode_SMD:D_SMA', '= "SMA(DO-214AC)"'),
        ('SOD-123', 'Diode_SMD:D_SOD-123', '= "SOD-123"'),
        ('SMC(DO-214AB)', 'Diode_SMD:D_SMC', '= "SMC(DO-214AB)"'),
        ('SOD-123FL', 'Diode_SMD:D_SOD-123F', '= "SOD-123FL"'),
        ('SMA', 'Diode_SMD:D_SMA', '= "SMA"'),
        ('SOD-523', 'Diode_SMD:D_SOD-523', '= "SOD-523"'),
        ('SMB', 'Diode_SMD:D_SMB', '= "SMB"'),
        ('SMC', 'Diode_SMD:D_SMC', '= "SMC"'),
        ('DO-214AC(SMA)', 'Diode_SMD:D_SMA', '= "DO-214AC(SMA)"'),
        ('DO-214AA(SMB)', 'Diode_SMD:D_SMB', '= "DO-214AA(SMB)"'),
    ]

def capacitor_packages():
    return [
        ('0402', 'Capacitor_SMD:C_0402_1005Metric', 'like "%402"'),
        ('0603', 'Capacitor_SMD:C_0603_1608Metric', 'like "%603"'),
        ('0805', 'Capacitor_SMD:C_0805_2012Metric', 'like "%805"'),
        ('1206', 'Capacitor_SMD:C_1206_3216Metric', 'like "%1206"'),
    ]


def ferritebead_packages():
    return [
        ('0402', 'Inductor_SMD:L_0402_1005Metric', 'like "%402"'),
        ('0603', 'Inductor_SMD:L_0603_1608Metric', 'like "%603"'),
        ('0805', 'Inductor_SMD:L_0805_2012Metric', 'like "%805"'),
        ('1206', 'Inductor_SMD:L_1206_3216Metric', 'like "%1206"'),
]

def led_packages():
    return [
    ('0402', 'LED_SMD:LED_0402_1005Metric', 'like "%402"'),
    ('0603', 'LED_SMD:LED_0603_1608Metric', 'like "%603"'),
    ('0805', 'LED_SMD:LED_0805_2012Metric', 'like "%805"'),
    ('1206', 'LED_SMD:LED_1206_3216Metric', 'like "%1206"'),
]

def transistor_packages():
    return [
    ('SOT-23', 'Package_TO_SOT_SMD:SOT-23', '= "SOT-23"'),
    ('SOT-323', 'Package_TO_SOT_SMD:SOT-323_SC-70', '= "SOT-323"'),
    ('SOT-223', 'Package_TO_SOT_SMD:SOT-223-3_TabPin2', '= "SOT-223"'),
    ('SOT-89-3', 'Package_TO_SOT_SMD:SOT-89-3', '= "SOT-89-3L"'),
    ('SOT-89-3', 'Package_TO_SOT_SMD:SOT-89-3', '= "SOT-89"'),
]