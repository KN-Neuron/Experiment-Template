from dataclasses import dataclass

from data_acquisition.gui.event_types import Key

from .constants import (
    BLOCK_COUNT,
    CONTINUE_SCREEN_ADVANCE_KEY,
    CONTINUE_SCREEN_TEXT,
    FIXATION_CROSS_TIMEOUT_RANGE_MILLIS,
    PAUSE_SCREEN_END_ANNOTATION,
    PAUSE_SCREEN_START_ANNOTATION,
    PAUSE_SCREEN_TEXT,
    PAUSE_UNPAUSE_KEY,
    RELAX_SCREEN_END_ANNOTATION,
    RELAX_SCREEN_START_ANNOTATION,
    RELAX_SCREEN_TIMEOUT_MILLIS,
    SENTENCE_SCREEN_ADVANCE_KEY,
    SENTENCE_SCREEN_END_ANNOTATION,
    SENTENCE_SCREEN_START_ANNOTATION,
    SENTENCE_SCREEN_TIMEOUT_MILLIS,
    SENTENCES_IN_BLOCK_COUNT,
)

fixation_cross_timeout_range_start_millis, fixation_cross_timeout_range_end_millis = (
    FIXATION_CROSS_TIMEOUT_RANGE_MILLIS
)


@dataclass
class Config:
    block_count: int = BLOCK_COUNT
    sentence_count: int = SENTENCES_IN_BLOCK_COUNT

    do_show_continue_screen: bool = True
    continue_screen_text: str = CONTINUE_SCREEN_TEXT
    continue_screen_advance_key: Key = CONTINUE_SCREEN_ADVANCE_KEY

    sentence_screen_advance_key: Key = SENTENCE_SCREEN_ADVANCE_KEY
    sentence_screen_timeout_millis: int = SENTENCE_SCREEN_TIMEOUT_MILLIS
    sentence_screen_start_annotation = SENTENCE_SCREEN_START_ANNOTATION
    sentence_screen_end_annotation = SENTENCE_SCREEN_END_ANNOTATION

    fixation_cross_timeout_range_start_millis: int = (
        fixation_cross_timeout_range_start_millis
    )
    fixation_cross_timeout_range_end_millis: int = (
        fixation_cross_timeout_range_end_millis
    )

    pause_unpause_key: Key = PAUSE_UNPAUSE_KEY
    pause_screen_text: str = PAUSE_SCREEN_TEXT
    pause_screen_start_annotation: str = PAUSE_SCREEN_START_ANNOTATION
    pause_screen_end_annotation: str = PAUSE_SCREEN_END_ANNOTATION

    relax_screen_timeout_millis: int = RELAX_SCREEN_TIMEOUT_MILLIS
    relax_screen_start_annotation: str = RELAX_SCREEN_START_ANNOTATION
    relax_screen_end_annotation: str = RELAX_SCREEN_END_ANNOTATION
