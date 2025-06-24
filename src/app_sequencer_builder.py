import itertools
from copy import copy
from pathlib import Path
from typing import Sequence

from data_acquisition.eeg_headset import EEGHeadset
from data_acquisition.gui import Gui
from data_acquisition.sequencers import BlockScreenSequencer, ScreenSequencer

from .config import Config
from .sentence_sequencer import SentenceSequencer
from .sentences import Sentences, load_sentences


class AppSequencerBuilder:
    def __init__(
        self, *, gui: Gui, config: Config, headset: EEGHeadset, participant_id: str
    ):
        self._gui = gui
        self._config = config
        self._headset = headset
        self._participant_id = participant_id

    def set_up_app_sequencer(self) -> ScreenSequencer[None]:
        self._set_up_save_directory()

        sentences = load_sentences()
        sequencers = self._build_sequencers_from_sentences(sentences)

        return BlockScreenSequencer(
            sequencers=sequencers,
            block_start_callback=lambda _: self._headset.start(),
            block_end_callback=lambda block_number: self._headset.stop_and_save_at_path(
                self._eeg_save_dir / f"{block_number}_raw.fif"
            ),
        )

    def _set_up_save_directory(self) -> None:
        self._eeg_save_dir = Path("data") / self._participant_id
        self._eeg_save_dir.mkdir(parents=True)

    def _build_sequencers_from_sentences(
        self, sentences: Sentences
    ) -> Sequence[ScreenSequencer[None]]:
        sequencers: list[ScreenSequencer[None]] = []

        sentences_in_blocks = itertools.islice(
            itertools.cycle([sentences.polish, sentences.english]),
            self._config.block_count,
        )

        for idx, sentences_in_block in enumerate(sentences_in_blocks):
            config = copy(self._config)
            config.do_show_continue_screen = idx != 0

            sequencer = SentenceSequencer(
                gui=self._gui,
                eeg_headset=self._headset,
                config=config,
                sentences=sentences_in_block,
            )

            sequencers.append(sequencer)

        return sequencers
