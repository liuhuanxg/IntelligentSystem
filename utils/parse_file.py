#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# 选择题
choice_questions = [
    {
        "title": "在一密闭容器中充入一定量的 N2和H2，经测定反应开始后的 2s内氢气的平均速率: v()=0.45mol/(Ls)，则2s末NH3的浓度为",
        "answer": "B",
        "options": {
            "A": "0.50mol/L",
            "B": "0.60mol/L",
            "C": "0.45mol/L",
            "D": "0.55mol/L ",
        }
    },
    {
        "title": "仅改变下列一个条件，通过提高活化分子的百分率来提高反应速率的是:",
        "answer": "A",
        "options": {
            "A": "加热",
            "B": "加压",
            "C": "加催化剂",
            "D": "加大反应物浓度",
        }
    },
    {
        "title": "下列反应及其平衡常数为:H₂(g)+S(s)=HzS(g) K;S(s)+O2(g)=SO2(g) K2°则反应Hz(g)+SOz(g)=H,S(g)+O2(g)的平衡常数是",
        "answer": "B",
        "options": {
            "A": "K1°+K2°",
            "B": "K1°-K2°",
            "C": "K1°xK2°",
            "D": "K1°/K2°",
        }
    },
    {
        "title": "反应A(g)+3B(g)、2C(g)+2D(g)，在不同情况下测得反应速率，其中反应速率最快的是",
        "answer": "B",
        "options": {
            "A": "vD)=0.4 mol/(L·S)",
            "B": "(C)=0.5mol/(L·S) ",
            "C": "(B)=0.6mol/(L.S)",
            "D": "(A)=0.15mol/(L.S)",
        }
    },
    {
        "title": "在一固定容积的密闭容器中充入2molA和1molB发生反应2A(g)+B(g) xC(g)达到平衡后体积分数为w%，若维持容器体积和温度不变，按06molA03molB14molc为起始物质，达到平衡后体积分数仍为W%，则X的值为",
        "answer": "B",
        "options": {
            "A": "1",
            "B": "2",
            "C": "4",
            "D": "5",
        }
    },
    {
        "title": "X(g)3Y(g)2W(g)M(g)H=-akJmol-1(a>0)。一定温度下，在体积恒定的密闭容器中，加入1molX(g)与1molY(g)，下列说法正确的是",
        "answer": "C",
        "options": {
            "A": "充分反应后，放出热量为akJ",
            "B": "当反应达到平衡状态时，x与W的物质的量浓度之比一定为1:2",
            "C": "当X的物质的量分数不再改变，表明该反应已达平衡",
            "D": "若增大Y的浓度，正反应速率增大，逆反应速率减小",
        }
    },
    {
        "title": "将H2(g)和Br2(g)充入恒容密闭容器,恒温下发生反应H(g)+Br2(g)=2HBr(g)H<0,平衡时Br2(g)的转化率为a;若初始条件相同,绝热下进行上述反应，平衡时Br2(g)的转化率为b。a与b的关系是",
        "answer": "A",
        "options": {
            "A": "a>b",
            "B": "a=b",
            "C": "a<b",
            "D": "无法确定",
        }
    },
    {
        "title": "下列常用数据中，通常不能通过化学手册自接查得的是",
        "answer": "B",
        "options": {
            "A": "弱酸的标准解离常数",
            "B": "盐的标准水解常数;",
            "C": "难溶电解质的标准溶度积常数;",
            "D": "弱碱的标准解离常数",
        }
    },
    {
        "title": "下列配合物中，属于螯合物的是",
        "answer": "A",
        "options": {
            "A": "[Ni(en)2]Cl",
            "B": "K2[PiC16]",
            "C": "(NH4)[Cr(NH3)2(SCN)4]",
            "D": "Li[AIH4]",
        }
    },
    {
        "title": "Co(NH3)5H20]Cl3的正确命名是",
        "answer": "C",
        "options": {
            "A": "一水·五氨基氯化钴",
            "B": "三氯化一水五氨合钴(I) ",
            "C": "三氯化五氨一水合钴(Ⅲ)",
            "D": "三氯化一水五氨合钴(I)",
        }
    },
    {
        "title": "关于螯合物，下列叙述正确的是",
        "answer": "C",
        "options": {
            "A": "鳌合物是一类很稳定的配合物，很少出现分级配合的现象; ",
            "B": "合剂均为有机物;",
            "C": "螯合剂的配位原子三面必须相隔2-3个非配位原子以形成较稳定的五元环或六元环螯合物;",
            "D": "形成整合物时在配位原子附近必须有足够的空间使金属离子进入整合剂结构的一定位置。",
        }
    },
    {
        "title": "下列有关实验室制取气体的反应中，其原理不属于氧化还原反应的是",
        "answer": "",
        "options": {
            "A": "实验室中用稀硫酸与锌粒反应制取H2",
            "B": "实验室中用浓盐酸与二氧化锰加热制Cl2",
            "C": "实验室中用高锰酸钾加热分解制取02",
            "D": "实验室中用稀盐酸与石灰石反应制取CO2",
        }
    },
    {
        "title": "为了提高cO在反应cO+H2 O( g )←→CO2+ H2中的转化率,可以",
        "answer": "B",
        "options": {
            "A": "增加 CO 的浓度",
            "B": "增加水蒸气的浓度",
            "C": "按比例增加水蒸气和 co 的浓度",
            "D": "三种办法都行",
        }
    },
    {
        "title": "用浓度表示溶液中化学平衡时,平衡常数表示式只在浓度不太大的时候适用,这是因为高浓度时",
        "answer": "D",
        "options": {
            "A": "浓度与活度的偏差较明显",
            "B": "溶剂的体积小于溶液体积",
            "C": "平衡定律不适用",
            "D": "还有其它化学平衡存在",
        }
    },
    {
        "title": "密封容器中A,B,C三种气体建立了化学平衡: A + B ←→ C 、相同温度下体积缩小2/3,则平衡常数 Kp 为原来的",
        "answer": "D",
        "options": {
            "A": "3倍",
            "B": "9倍",
            "C": "2倍",
            "D": "不变",
        }
    },
]

# 填空题
judgment_questions = [
    {
        "title": "CaCO 3在常温下不分解，是因为其分解反应为吸热反应；在高温下分解，是因为此时分解放热。",
        "answer": "0",
    },
    {
        "title": "酸性水溶液中不含OH -，碱性水溶液中不含H +",
        "answer": "0",
    },
    {
        "title": "需要加热才能进行的化学反应不一定是吸热反应。",
        "answer": "1",
    }, {
        "title": "通常，反应速率常数k 与浓度无关，而与温度有关。",
        "answer": "1",
    }, {
        "title": "在一定温度下，改变溶液的pH值，水的离子积不变。",
        "answer": "1",
    }, {
        "title": "AgCl在NaCl溶液中的溶解度比在纯水中的溶解度小",
        "answer": "0",
    }, {
        "title": "在一定的温度下，浓度发生变化时，速率常数保持不变。",
        "answer": "1",
    },
    {
        "title": "升温可以使吸热反应速率增大，放热反应速率减小。",
        "answer": "0",
    },
    {
        "title": "复杂反应的反应速率取决于反应速率最慢的基元反应",
        "answer": "1",
    }, {
        "title": "无论是吸热反应还是放热反应，只要升温，速率常数就会增大",
        "answer": "1",
    }, {
        "title": "在一定条件下，给定反应的平衡常数越大，反应速率越快",
        "answer": "0",
    },
    {
        "title": "由于Ksp和Qi表达式几乎相同，所以它们的含义完全相同",
        "answer": "0",
    }, {
        "title": "任一化学反应的速率方程，都可根据化学方程式写出",
        "answer": "0",
    }, {
        "title": "电子云是描述核外某空间电子出现的几率密度的概念",
        "answer": "1",
    },
    {
        "title": "系统经历一个循环，无论多少步骤，只要回到初始状态，其热力学的变为零",
        "answer": "1",
    },
    {
        "title": "反应活化能越小，反应速率越大",
        "answer": "0",
    },
    {
        "title": "配合物中中心离子的配位数是指配位体的总数",
        "answer": "1",
    },
    {
        "title": "平衡常数和转化率都能表示反应进行的程度，但平衡常数与反应物的起始浓度无关，而转化率与反应物的起始浓度有关。",
        "answer": "0",
    }, {
        "title": "单质的生成焓都为0.",
        "answer": "0",
    }, {
        "title": "弱电解质的解离度随弱电解质浓度的降低而增大",
        "answer": "1",
    }, {
        "title": "某温度时标准平衡常数越大，表明反应在此温度时越能快速完成",
        "answer": "0",
    }, {
        "title": "压力的改变对任何物质的溶解度都影响不大",
        "answer": "0",
    }, {
        "title": "溶解度是指饱和溶液中溶质和溶剂的相对含量",
        "answer": "0",
    }, {
        "title": "凡吉布斯自由能降低的过程一定是自发过程",
        "answer": "1",
    }, {
        "title": "用容量瓶配制溶液时，瓶内干燥与否不影响最终结果",
        "answer": "1",
    }, {
        "title": "难溶电解质的不饱和溶液中不存在沉淀溶解平衡",
        "answer": "1",
    }
]


def main():
    data = {
        "choice_questions": [],
        "judgment_questions": []
    }
    total_count = 20
    count1 = 10
    for i in range(total_count):
        if i < count1:
            while True:
                question = random.choice(choice_questions)
                if question not in data["choice_questions"]:
                    data["choice_questions"].append(question)
                    break
        else:
            while True:
                question = random.choice(judgment_questions)
                if question not in data["judgment_questions"]:
                    data["judgment_questions"].append(question)
                    break
    total_score = 0
    print("{}---{}---{}".format("*" * 10, "开始答题", "*" * 10))
    index = 1
    for q_type, questions in data.items():
        for question in questions:
            print("题目{}：{}".format(index, question.get("title")))
            if q_type == "choice_questions":
                print("选项：")
                for k, option in question.get("options", {}).items():
                    print("\t{}: {}".format(k, option))
            else:
                print("\t认为正确请输入【1】，认为错误请输入【0】")
            answer = input("请输入答案：")
            if answer == question.get("answer"):
                total_score += 5
            index += 1
            print("正确答案：{}".format(question.get("answer")))
            print("*" * 40)
    print("{}---{}---{}".format("*" * 10, "结束答题", "*" * 10))
    print("总得分:{}".format(total_score))
    if total_score < 70:
        print("复习不过关")
    else:
        print("非常棒")


if __name__ == '__main__':
    main()
