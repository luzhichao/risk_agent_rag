# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from utils import time_utils


def _wait_next_millis(last_timestamp):
    timestamp = time_utils.now_time()
    while timestamp == last_timestamp:
        timestamp = time_utils.now_time()
    return timestamp


class Snowflake:
    # 起始时间戳 (2024-01-01)
    EPOCH = 1704067200000

    # 各部分占用位数
    WORKER_ID_BITS = 5
    DATA_CENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    # 最大值
    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
    MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)

    # 偏移量
    WORKER_ID_SHIFT = SEQUENCE_BITS
    DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS

    def __init__(self, worker_id: int = 1, data_center_id: int = 1):
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError("worker Id 超出范围")
        if data_center_id > self.MAX_DATA_CENTER_ID or data_center_id < 0:
            raise ValueError("data center Id 超出范围")

        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate(self) -> int:
        timestamp = time_utils.now_time()

        if timestamp < self.last_timestamp:
            raise Exception("时间回退，无法生成ID")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                timestamp = _wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
            (self.data_center_id << self.DATA_CENTER_ID_SHIFT) | \
            (self.worker_id << self.WORKER_ID_SHIFT) | \
            self.sequence


# 全局单例（项目中只用这一个实例）
snowflake = Snowflake(worker_id=1, data_center_id=1)


def next_id() -> str:
    """
    生成字符串雪花ID
    @author: Luzhichao
    @date: 2026-05-07
    """
    return str(snowflake.generate())
