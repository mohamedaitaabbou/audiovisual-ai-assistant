audiovisual_knowledge = {

    "ccu": """
    CCU stands for Camera Control Unit.

    In professional television broadcasting, it is part of the camera chain.
    It manages camera operating parameters such as iris, gain, white balance,
    black level, color balance and other image settings depending on the system.

    In multi-camera production, CCUs help match cameras for consistent image quality.
    They may also provide return video, intercom, tally and other broadcast signals.
    """,

    "rcp": """
    RCP stands for Remote Control Panel.

    It is the operator's remote interface for adjusting camera parameters,
    usually through a connected CCU.

    It allows vision operators to remotely control image settings such as iris,
    white balance, gain, black level and color adjustments.
    """,

    "sdi": """
    SDI stands for Serial Digital Interface.

    SDI is a professional digital video interface widely used in television
    broadcasting and production facilities.

    It commonly transports video, embedded audio and ancillary data over
    coaxial cables using BNC connectors, or over fiber in some systems.

    Common SDI families include SD-SDI, HD-SDI, 3G-SDI, 6G-SDI,
    12G-SDI and other standards depending on video format and equipment.

    SDI is commonly used to connect cameras, vision mixers, monitors,
    routers, servers and broadcast equipment.
    """,

    "hdmi": """
    HDMI stands for High-Definition Multimedia Interface.

    HDMI transmits digital video and audio through a single interface.

    It is widely used in consumer equipment, computers, monitors,
    projectors and some professional audiovisual devices.

    HDMI can carry video, audio and additional data depending on the version
    and connected equipment.

    Unlike traditional broadcast SDI connections, HDMI connectors are not
    designed with the same locking mechanism commonly used by BNC connectors.
    """,

    "white balance": """
    White Balance is the process of adjusting camera color settings so that
    white objects appear neutral under different lighting conditions.

    It helps maintain accurate colors and consistent appearance between cameras.

    White balance can be adjusted manually or automatically depending
    on the camera and production workflow.
    """,

    "iris": """
    Iris controls the amount of light entering the camera lens.

    It affects image exposure and is commonly measured in f-stops.

    Opening the iris allows more light to reach the sensor.
    Closing the iris reduces the amount of light.
    """,

    "gain": """
    Gain amplifies the camera signal to increase image brightness
    when additional sensitivity is required.

    Higher gain may introduce more visible noise into the image.

    Gain settings depend on the camera system and shooting conditions.
    """,

    "playout": """
    Playout is the process and system used to play television content
    for broadcast or transmission.

    Broadcast playout systems may include video servers, playlists,
    automation software, graphics, audio, scheduling and monitoring.

    Playout operators manage media playback, scheduled content,
    transitions between clips, live events and transmission continuity.

    Playout systems can operate manually or through automation,
    depending on the broadcast workflow.
    """,

       "vision mixer": """
    A Vision Mixer, also called a Video Switcher, is used to select
    and combine video sources during live television production.

    PROGRAM (PGM):
    The Program bus carries the video currently sent to the main output.

    PREVIEW (PVW):
    The Preview bus allows operators to select and check the next source
    before sending it to Program.

    CUT:
    CUT is an instantaneous transition from the current Program source
    to the selected Preview source.

    AUTO TRANSITION:
    Automatically performs a transition between Preview and Program.
    Common transitions include Mix, Dissolve and Wipe.

    M/E (Mix Effects):
    An M/E is a processing section of a vision mixer.
    It can combine multiple video sources and create layered compositions.

    KEY:
    Keying allows one video source to be placed over another.
    Common types include Chroma Key and Luma Key.

    DSK (Downstream Keyer):
    A DSK adds graphics or other keyed elements over the final
    Program output, such as logos and lower thirds.

    Other functions may include DVE effects, transitions,
    source selection and multiple M/E buses.
    """,

    "vizrt": """
    Vizrt is a broadcast graphics and visual storytelling technology provider.

    Its systems are used in television production for real-time graphics,
    virtual sets, data-driven graphics and broadcast visual presentation.

    Vizrt workflows may include graphics templates, newsroom integration,
    rendering engines, control interfaces and automation.

    Typical broadcast graphics include lower thirds, headlines,
    tickers, maps, statistics, full-screen graphics and virtual elements.

    Specific functions depend on the product and system configuration.
    """,

    "prompter": """
    A Teleprompter displays scrolling text that presenters read
    while looking directly toward the camera.

    It helps presenters deliver scripts naturally without looking
    away from the camera.

    Prompter systems may be controlled by an operator who adjusts
    text speed and timing according to the presenter.
    """
}


question_keywords = {

    "ccu": [
        "ccu", "camera control unit", "camera control",
        "camera settings", "camera parameters"
    ],

    "rcp": [
        "rcp", "remote control panel", "camera remote control"
    ],

    "sdi": [
        "sdi", "serial digital interface", "3g sdi",
        "12g sdi", "hd sdi", "bnc", "sd-sdi"
    ],

    "hdmi": [
        "hdmi", "high-definition multimedia interface"
    ],

    "white balance": [
        "white balance", "color temperature", "colour temperature"
    ],

    "iris": [
        "iris", "camera iris", "aperture", "f-stop"
    ],

    "gain": [
        "gain", "camera gain", "video gain"
    ],

    "playout": [
        "playout", "broadcast playout", "video server",
        "playlist", "broadcast automation"
    ],

    "vision mixer": [
    "vision mixer", "video switcher",
    "program", "pgm", "program bus",
    "preview", "pvw", "preview bus",
    "cut", "auto transition",
    "mix", "dissolve", "wipe",
    "m/e", "mix effects",
    "key", "keying", "chroma key",
    "luma key", "dsk", "downstream keyer"
    ],

    "vizrt": [
        "vizrt", "broadcast graphics", "real-time graphics",
        "lower third", "ticker", "virtual set"
    ],

    "prompter": [
        "prompter", "teleprompter", "prompting"
    ]
}
