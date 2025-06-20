from datetime import datetime
from threading import Thread

from data_acquisition.eeg_headset import MockEEGHeadset
from data_acquisition.experiment_runner import ExperimentRunner
from data_acquisition.gui import PygameGui
from data_acquisition.gui.display_mode import FullscreenDisplayMode, WindowedDisplayMode

from src.app_sequencer_builder import AppSequencerBuilder
from src.config import Config
from src.constants import RELAX_SCREEN_TIMEOUT_MILLIS, SENTENCES_IN_BLOCK_COUNT

DEBUG_SENTENCES_IN_BLOCK_COUNT = 3
DEBUG_RELAX_SCREEN_TIMEOUT_MILLIS = 5 * 1000


def run(*, debug: bool) -> None:
    participant_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )  # TODO: zamienic na ID z ankiety

    display_mode = (
        WindowedDisplayMode(width=800, height=600) if debug else FullscreenDisplayMode()
    )
    gui = PygameGui(display_mode=display_mode, window_title="NeuroGuard")

    headset = MockEEGHeadset()

    config = Config(
        sentence_count=(
            DEBUG_SENTENCES_IN_BLOCK_COUNT if debug else SENTENCES_IN_BLOCK_COUNT
        ),
        relax_screen_timeout_millis=(
            DEBUG_RELAX_SCREEN_TIMEOUT_MILLIS if debug else RELAX_SCREEN_TIMEOUT_MILLIS
        ),
    )

    app_sequencer_builder = AppSequencerBuilder(
        gui=gui, config=config, headset=headset, participant_id=participant_id
    )
    sequencer = app_sequencer_builder.set_up_app_sequencer()

    runner = ExperimentRunner(
        gui=gui, screen_sequencer=sequencer, end_callback=gui.stop
    )

    Thread(target=runner.run).start()
    gui.start()
