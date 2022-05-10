#!/usr/bin/env python
# -*- coding: utf-8 -*-

option = {
    "title": {
        "text": 'Referer of a Website',
        "subtext": 'Fake Data',
        "left": 'center'
    },
    "tooltip": {
        "trigger": 'item'
    },
    "legend": {
        "orient": 'vertical',
        "left": 'left'
    },
    "series": [
        {
            "name": 'Access From',
            "type": 'pie',
            "radius": '50%',
            "data": [
                {"value": 1048, "": 'Search Engine'},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
}
