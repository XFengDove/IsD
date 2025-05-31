import json
from random import choice
from Secure import SecuerT

with open("UserData.json", "r", encoding="utf-8") as f:
    UserData = json.load(f)
    print(UserData)
def New_UserData(UserData:dict[str]):
    pass

New_UserData(UserData)
class DaCa:
    def __init__(self, UserData=UserData):
        self.ResA = 0.1
        self.ResB = 50
        self.UserData = UserData
        Role = UserData["User"]["Role"]
        Spell_Bonus = UserData["User"]["Role"]["法术伤害加成"]
        self.Materiel= UserData["User"]["Materiel"]
        self.Jewelry = UserData["User"]["Materiel"]["Jewelry"]

        self.Health=Role["生命值"]
        self.MaxMana=Role["MaxMana"]
        self.NowMana=Role["NowMana"]

        self.Phy_Attack = Role["物理攻击力"]
        self.Spell_Attack = Role["法术攻击力"]
        self.Crit_Strike = Role["暴击率"]
        self.Crit_Damage = Role["暴击伤害"]

        self.Fire = Spell_Bonus["火焰"]
        self.Water = Spell_Bonus["水"]
        self.Ice = Spell_Bonus["冰"]
        self.Light = Spell_Bonus["光明"]

        self.Phy_Resistance = Role["物理抗性"]
        self.Spell_Resistance = Role["法术抗性"]
        self.AllDamage_Bonus = Role["全伤害加成"]
    def GetDamageTapy(self,)->list:

        return []
    def Damage(self,Tage:list[str]):

        if Tage[0]=="Phy":
            BaseDamage = self.Phy_Attack * (1 + self.Crit_Damage) if self.BigDam() else self.Phy_Attack
            PhyDamage = BaseDamage * (1 - self.Resistance(self.Phy_Resistance))
            return int(PhyDamage*self.AllDamage_Bonus)
        elif Tage[0]=="Spell":
            BaseDamage = self.Spell_Attack* (1 + self.Crit_Damage) if self.BigDam() else self.Spell_Attack
            if Tage[1]=="Phy":
                All_Res=self.Resistance(self.Phy_Resistance)+self.Resistance(self.Spell_Resistance)
                SpellPhyDamage=BaseDamage*(1-All_Res)
                return int(SpellPhyDamage*self.AllDamage_Bonus)
            elif Tage[1]=="Spell":
                SpellDamage=BaseDamage*(1-self.Resistance(self.Spell_Resistance))
                if Tage[2]=="Fire":
                    return int(SpellDamage*(1+self.Fire)*self.AllDamage_Bonus)
                elif Tage[2]=="Water":
                    return int(SpellDamage*(1+self.Water)*self.AllDamage_Bonus)
                elif Tage[2]=="Ice":
                    return int(SpellDamage*(1+self.Ice)*self.AllDamage_Bonus)
                elif Tage[2]=="Light":
                    return int(SpellDamage*(1+self.Light)*self.AllDamage_Bonus)
        return None

    def Resistance(self, Num: int)->float:
        """计算抗性实际减伤百分比

        :param Num:
        :return:
        """
        Tier = Num // self.ResB
        Other = Num % self.ResB
        if Tier == 0:
            return float(format(self.ResA / self.ResB * Other, ".2f"))
        else:
            Resis = 0
            for i in range(1, Tier + 1):
                Resis += (1 - Resis) * self.ResA
            return float(format(Resis + (self.ResA / self.ResB * Other), ".2f"))

    def BigDam(self):
        """判断角色攻击是否暴击

        :return:
        """
        A = int(self.UserData["User"]["Role"]["暴击率"] * 100)
        Chouse_List = [1 for _ in range(A)] + [0 for _ in range(100 - A)]
        return True if choice(Chouse_List) == 1 else False


if __name__ == "__main__":
    Ud=DaCa()
    # print(Ud.Resistance(20))
    # print(Ud.Damage())
