from threading import Thread
from typing import cast

from data_acquisition.eeg_headset import MockEEGHeadset
from data_acquisition.experiment_runner import ExperimentRunner
from data_acquisition.gui import PygameGui
from data_acquisition.gui.display_mode import FullscreenDisplayMode, WindowedDisplayMode
from data_acquisition.pre_experiment_survey import PreExperimentSurvey

from .app_sequencer_builder import AppSequencerBuilder
from .config import Config
from .constants import (
    BLOCK_COUNT,
    DEBUG_BLOCK_COUNT,
    DEBUG_RELAX_SCREEN_TIMEOUT_MILLIS,
    DEBUG_SENTENCES_IN_BLOCK_COUNT,
    RELAX_SCREEN_TIMEOUT_MILLIS,
    SENTENCES_IN_BLOCK_COUNT,
    SURVEY_CONFIG_PATH,
    SURVEY_PARTICIPANT_ID_KEY,
)


def run(
    *,
    brainaccess_cap_name: str,
    do_use_debug_mode: bool = False,
    do_use_mock_headset: bool = False,
) -> None:
    if do_use_mock_headset:
        headset = MockEEGHeadset()
    else:
        from data_acquisition.eeg_headset.brainaccess import BrainAccessV3Headset
        from data_acquisition.eeg_headset.brainaccess.devices import (
            BRAINACCESS_MAXI_32_CHANNEL,
        )

        headset = BrainAccessV3Headset(
            device_name=brainaccess_cap_name,
            device_channels=BRAINACCESS_MAXI_32_CHANNEL,
        )

    survey = PreExperimentSurvey(config_file_path=SURVEY_CONFIG_PATH)
    responses = survey.start_and_get_responses()
    participant_id = cast(str, responses.get(SURVEY_PARTICIPANT_ID_KEY))

    display_mode = (
        WindowedDisplayMode(width=800, height=600)
        if do_use_debug_mode
        else FullscreenDisplayMode()
    )
    gui = PygameGui(display_mode=display_mode, window_title="NeuroGuard")

    config = Config(
        block_count=(DEBUG_BLOCK_COUNT if do_use_debug_mode else BLOCK_COUNT),
        sentence_count=(
            DEBUG_SENTENCES_IN_BLOCK_COUNT
            if do_use_debug_mode
            else SENTENCES_IN_BLOCK_COUNT
        ),
        relax_screen_timeout_millis=(
            DEBUG_RELAX_SCREEN_TIMEOUT_MILLIS
            if do_use_debug_mode
            else RELAX_SCREEN_TIMEOUT_MILLIS
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
