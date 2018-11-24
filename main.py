import PyPDF2, re


class Agent(object):
    """docstring for Agent."""
    def __init__(self):
        super(Agent, self).__init__()
        self.firstName = ""
        self.middleName = ""
        self.lastName = ""
        self.id = 0

    def setNames(self, arg):
        if len(arg) == 2:
            self.firstName = arg[0]
            self.lastName = arg[1]

        elif len(arg) == 3:
            self.firstName = arg[0]
            self.middleName = arg[1]
            self.lastName = arg[2]

        elif len(arg) == 1:
            self.firstName = arg[0]

    def setId(self, arg):
        if arg[0] == "(":
            arg = arg[1:]

        if arg[-1] == ")":
            arg = arg[:-1]

        self.id = arg

    def __str__(self):
        return "{} {} {} {}".format(self.firstName, self.middleName, self.lastName, self.id)


def main():

    contents = ""
    agents = []

    with open("../stats/adams.PDF", "rb") as file:
        pdf = PyPDF2.PdfFileReader(file)

        for page in range(pdf.getNumPages()):
            contents += pdf.getPage(page).extractText()

        agentList = re.findall(r"(([A-z,\",',\.]+ )+([A-z,\",',\.])+ \(\d+\))", contents)
        for item in agentList:
            newAgent = Agent()

            names = re.findall(r"([A-z,\",',\.]+)", item[0])
            id = re.findall(r"(\(\d+\))", item[0])

            newAgent.setNames(names)
            newAgent.setId(id[0])

            print(newAgent)
        # print(asdf)



main()
