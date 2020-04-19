# -*- coding : utf-8 -*-
import os,sys,time,threading,re,random
from colors import colors
from filters import filters
from banners import banners
from users import users
class PyAnti():
    def __init__(self):
        self.tehtit_list = {}
        self.risk_list  = {}

        self.ignore_list = [os.getcwd(),os.getcwd()+"/filters",os.getcwd()+"/karantina"] # Ekleme yapabilirsiniz ( Bu kısımları atlama sebebimiz karantina'da karantinaya alınan dosyaları çalıştırılamaz hale getirip saklamak , filters 'de ise filterler var yani orayı zaralı yazılım olarak görecektir .. )
        self.scan_syspath = False
        with open("white.list","a+") as white:
            white.seek(0)
            self.white_list=white.read().splitlines()
        
        
    def tara(self,konum="/home"):
        for o_o in os.walk(konum):
            if o_o[2]:
                self.o_o = o_o
                for dosya in o_o[2]:
                    if dosya.endswith(".py") or dosya.endswith(".pyw"): # Dosya uzantısı .py veya .pyw ise devam et ( güvenliği azaltacaktır ne yazık ki ... )
                        if o_o[0] not in self.ignore_list: # eger self.konum ignore_list 'in icersindeyse atla (ignore_list okunmayacaklar listesi)
                            if o_o[0]+dosya not in self.white_list:
                                self.dosya = dosya
                                self.konum = o_o[0]
                                self.tam_konum = self.konum+"/"+self.dosya
                                #print(self.tam_konum)
                                self.bakbakalim()
                

    def bakbakalim(self,konum=None):
        if not konum == None:
            self.tam_konum = konum
            
        if self.tam_konum in self.white_list:
            print(banners.unlem.format(colors.yesil+"whitelist elemanı atlanıyor !"+colors.normal))
            print(f"\n\t'{self.tam_konum}' \n\n\telemanı atlanıyor (PyAnti.white_list) | white.list ")

        
            
        elif not self.scan_syspath and ("/".join(self.tam_konum.split("/")[:-1]) in sys.path or "/".join(self.tam_konum.split("/")[:-2]) in sys.path or "/".join(self.tam_konum.split("/")[:-3]) in sys.path or "/".join(self.tam_konum.split("/")[:-4]) in sys.path or "/".join(self.tam_konum.split("/")[:-5]) in sys.path):
            print(banners.unlem.format("sys.path konumu atlanıyor ! | PyAnti().scan_syspath = False\n\t"+colors.cizik+self.tam_konum+colors.normal))

        else: # try: ekle
            try:
                
                with open(self.tam_konum) as oku:
                    oku = oku.read()
                print(colors.yesil+"Taranan konum : "+colors.normal+colors.egri+self.tam_konum+colors.normal)
                for filt in filters.filters:
                    note = re.search(filt[0],oku)
                    if not note == None:
                        start = note.start()
                        end = note.end()
                        if self.tam_konum in self.tehtit_list.keys():
                            ekle = self.tehtit_list[self.tam_konum]
                            ekle["tehtit"].append(filt[0])
                            ekle["aciklama"].append(filt[1])
                            ekle["risk"].append(filt[2])
                            ekle["aralik"].append([start,end])
                        else:
                            self.tehtit_list[self.tam_konum] = {"dosya":self.dosya , "konum":self.tam_konum , "tehtit":[filt[0]] , "aciklama": [filt[1]]  ,"risk" : [filt[2]] , "aralik":[[start,end]] }
                
                for key in self.tehtit_list.keys():
                    tehtit_sayisi = len(self.tehtit_list[key]["tehtit"])
                    if tehtit_sayisi > 1:
                        for i in range(tehtit_sayisi):
                            break_key = 0
                            risk = self.tehtit_list[key]["risk"][i]
                            if risk >= 5:
                                if not self.tehtit_list[key]["konum"] in self.risk_list.keys():
                                    self.risk_list[self.tam_konum] = self.tehtit_list[key]
                                    #print(self.tehtit_list[key])
                                    print("| Tehtit Listesine eklendi | | "+self.tam_konum)
                                    break
                        
            except Exception as hata:print("HATA : "+str(hata))

                

    def kapi():
        pass


    def isle(self):
        print(banners.pyanti)
        os.popen("notify-send -a 'PyAnti' 'Okunaklaştırılıyor' '5-10 risk değeri olan tüm betikler güzelleştiriliyor .'")
        for key in self.risk_list.keys():
            veri = self.risk_list[key]
            print(random.choice(colors.renkler)+banners.ayirac.format(veri["dosya"])+colors.normal)
            print("\tDosya  : "+veri["dosya"])
            print("\tKonum  : "+veri["konum"])
            print("\tBul Rs : "+str(len(veri["tehtit"])))
            for i in range(len(veri["tehtit"])):
                print()
                print("\tTehtit : "+veri["tehtit"][i])
                print("\tAçklam : "+veri["aciklama"][i])
                print("\tRISK   : "+str(veri["risk"][i]))
                print("\tAralik : "+str(veri["aralik"][i]))

            konum = veri["konum"]
            secenek = input(f"\n\t{konum} 'a ne  yapalım ? \n\n\t{colors.yesil}ENTER{colors.normal} = Hiçbirşey yapma\n\n\t{colors.cam}W{colors.normal} = White List'e ekle\n\n\t{colors.sari}K{colors.normal} = Karantinaya al\n\n\t{colors.kirmizi}S{colors.normal} = SIL\n\n\n\t[{os.getlogin()}] : ").strip().lower()
            if secenek == "w":
                try:
                    durum = f"WhiteList'e alındı ({os.getlogin()}/white.list) 'den silebilirsin !"
                    self.white_list.append(konum)
                    with open("white.list","a") as yaz:
                        yaz.write(konum+"\n")
                    print(banners.unlem.format(colors.yesil+"BeyazListeye eklendi ! ()"+colors.normal))
                except Exception as hata:
                    durum += f"\nSon Güncelleme : BeyazListeye eklenemedi ! Hata : {str(hata)}"
                    input(banners.x.format("HATA : "+str(hata)))


            elif secenek == "k":
                try:
                    if not os.path.exists("karantina"):
                        os.mkdir("karantina")
                    
                    
                    dosya = konum.split("/")[::-1][0]
                    durum = f"Karantinaya alınıyor ! Ilk Konum : {konum} | Son Konum : karantina/{dosya}"
                    with open(konum) as oku:
                        oku = "'''"+oku.read()+"'''"
                    with open("karantina/"+dosya,"w") as yaz:
                        yaz.write(oku)

                except Exception as hata:
                    durum += "\nSon Güncelleme : Karantinaya alınamadı , Dosya silinmedi ! Hata : "+str(hata)
                    input(banners.x.format("Karantinaya Alınamadı ! Hata :"+str(hata)))
                else: 
                    os.remove(konum)
                    print(banners.karantinaya_alindi)
                
            elif secenek == "s":
                try:
                    durum = f"{konum} siliniyor !"
                    os.remove(konum)
                except Exception as hata:
                    durum += "\nSon Güncelleme : Silinemedi ! Hata : "+str(hata)
                    input(banners.x.format("HATA : "+str(hata)))
                else:
                    print(banners.yok_edildi)
            
            else:
                durum = "İşlem Uygulanmadı !"

            
            
            
            
            
            # Dosyaya yazma eylemi
            if not os.path.exists("log"):
                os.mkdir("log")
            
            zaman = "{}.{}.{}_{}.{}".format(time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year,time.localtime().tm_hour,time.localtime().tm_min)
            log = open("log/"+zaman+".txt","a")
            print("\n\t - - - - - -- - - - - - - \n\n",file=log,flush=True)
            print("\tDosya  : "+veri["dosya"],file=log,flush=True)
            print("\tKonum  : "+veri["konum"],file=log,flush=True)
            print("\tBul Rs : "+str(len(veri["tehtit"])),file=log,flush=True)
            for i in range(len(veri["tehtit"])):
                print("\n",file=log,flush=True)
                print("\tTehtit : "+veri["tehtit"][i],file=log,flush=True)
                print("\tAçklam : "+veri["aciklama"][i],file=log,flush=True)
                print("\tRISK   : "+str(veri["risk"][i]),file=log,flush=True)
                print("\tAralik : "+str(veri["aralik"][i]),file=log,flush=True)
                print("\n\tDURUM  : "+str(durum),file=log,flush=True)

            log.close()




    def rapor(self):
        return {"low":self.tehtit_list,"up":self.risk_list}



if __name__ == "__main__":
    pyanti = PyAnti()
    pyanti.tara()
    pyanti.isle() # pynati.rapor() 'u güzelleşitirip silme seçeneklerini soracak

                    
