class DataTurnHelper:
    def getOption(self, index):
        try:
            return self.OptionList[index]
        except IndexError:
            return ""

    def getIndex(self, optionValue):
        try:
            return self.OptionList.index(optionValue)
        except ValueError:
            return -1


class ApprovalStatus(DataTurnHelper):
    OptionList = [
        "未提交",# 0
        "审核中",# 1
        "已审核",# 2
        "已撤回",# 3
        "已驳回",# 4
        "已拒绝" # 5
    ]
