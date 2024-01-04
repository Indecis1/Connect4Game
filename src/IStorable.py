# -*- coding: utf-8 -*-
from __future__ import annotations

import abc


class IStorable(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def load_from_json(json: dict, errors: list[str]) -> list[IStorable]:
        """
        Loads from json object
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save_to_json(self, data_to_saved: dict, errors: list[str]) -> dict:
        """
        Save to json object
        :return:
        """
        raise NotImplementedError
