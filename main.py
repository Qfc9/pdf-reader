import PyPDF2, re
from os import listdir

class Agent(object):
    """docstring for Agent."""
    def __init__(self):
        super(Agent, self).__init__()
        self.firstName = ""
        self.middleName = ""
        self.lastName = ""
        self.id = 0
        self.volume = 0.0
        self.officeId = 0
        self.county = 38

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

        self.firstName = self.firstName.replace('"', "'")
        self.middleName = self.middleName.replace('"', "'")
        self.lastName = self.lastName.replace('"', "'")

    def setId(self, arg):
        if arg[0] == "(":
            arg = arg[1:]

        if arg[-1] == ")":
            arg = arg[:-1]

        self.id = int(arg)

    def setVolume(self, arg):
        self.volume = float(arg[0][2:].replace(",", ""))

    def setOffice(self, arg):
        self.officeId = int(arg[1:])

    def setCounty(self, arg):
        self.county = arg.title()

    def getSQL(self):
        return "INSERT INTO `agents`(`id`, `mls_id`, `f_name`, `m_name`, `l_name`, `volume`, `office_id`, `county`) VALUES (NULL, {}, \"{}\", \"{}\", \"{}\", {}, {}, {});\n".format(self.id, self.firstName, self.middleName, self.lastName, self.volume, self.officeId, self.county)

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.county, self.firstName, self.middleName, self.lastName, self.volume, self.id, self.officeId)


def main():

    agents = []

    files = listdir("../stats")

    for countyId, file in enumerate(files):
        county = file[:-4]
        print(county)

        contents = ""

        with open("../stats/" + file, "rb") as file:
            pdf = PyPDF2.PdfFileReader(file)

            for page in range(pdf.getNumPages()):
                contents += pdf.getPage(page).extractText()

            # print(contents)
            contents = contents.replace("\n", "")

            agentList = re.findall(r"(([A-z,\",',\.]+ )+([A-z,\",',\.])+ \(\d+\))", contents)
            volume = re.findall(r"((\.\d+)(,\d{3})+)", contents)
            officeId = re.findall(r"(\)\d{4})", contents)

            for idx, item in enumerate(agentList):
                newAgent = Agent()

                names = re.findall(r"([A-z,\",',\.]+)", item[0])
                id = re.findall(r"(\(\d+\))", item[0])

                newAgent.setNames(names)
                newAgent.setId(id[0])
                newAgent.setVolume(volume[idx])
                newAgent.setOffice(officeId[idx])
                newAgent.county = countyId + 2

                agents.append(newAgent)

    print(len(agents))
    with open("sql.txt", "w") as file:
        for agent in agents:
            file.write(agent.getSQL())


main()
