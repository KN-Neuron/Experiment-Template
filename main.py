from src.run import run

DO_MAKE_IT_QUICKER = False
DO_USE_MOCK_HEADSET = True

BRAINACCESS_CAP_NAME = "BA MAXI 011"


if __name__ == "__main__":
    run(
        brainaccess_cap_name=BRAINACCESS_CAP_NAME,
        do_make_it_quicker=DO_MAKE_IT_QUICKER,
        do_use_mock_headset=DO_USE_MOCK_HEADSET,
    )
