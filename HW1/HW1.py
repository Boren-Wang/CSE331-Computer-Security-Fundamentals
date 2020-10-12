from collections import Counter

# Part 1
def keystream(text, key):
    res = ""
    count_non_alpha = 0
    for i in range(len(text)):
        if not text[i].isalpha():
            res += " "
            count_non_alpha += 1
        else:
            res += key[(i - count_non_alpha) % len(key)]
    return res

# print(keystream("Hello world123!", "SECURITY"))

def encrypt(plaintext, key):
    keystr = keystream(plaintext, key)
    # print(keystr)
    for i in range(len(plaintext)):
        if not plaintext[i].isalpha():
            print(plaintext[i], end="")
            continue
        a = 'A' if plaintext[i].isupper() else 'a'
        char = keystr[i]
        # print(char, end="")
        shift = ord(char) - ord('A')
        ciphertext = chr(ord(a) + (ord(plaintext[i]) - ord(a) + shift) % 26)
        print(ciphertext, end="")

# encrypt("ATTACKATDAWN", "LEMON")
# encrypt("Hello world123!", "SECURITY")
# print()
# encrypt("hell-o wor ld!", "SECURITY")

# Part 2
def decrypt(ciphertext, key):
    # 1. generate keystream
    keystr = keystream(ciphertext, key)

    # 2. generate plaintext
    for i in range(len(ciphertext)):
        if not ciphertext[i].isalpha():
            print(ciphertext[i], end="")
            continue
        a = 'A' if ciphertext[i].isupper() else 'a'
        char = keystr[i]
        # print(char, end="")
        shift = ord(char) - ord('A')
        plaintext = chr(ord(a) + (ord(ciphertext[i]) - ord(a) - shift) % 26)
        print(plaintext, end="")

# decrypt("LXFOPVEFRNHR", "LEMON")
# print()
# decrypt("Zinff ehpdh123!", "SECURITY")
# print()
# decrypt("zinf-f ehp dh!", "SECURITY")

# Part 3
from scipy.stats import chisquare

def part3(ciphertext, key_length):
    key = ""
    ciphertext_alpha = "".join(filter(str.isalpha, ciphertext)).upper()
    groups = get_groups(ciphertext_alpha, key_length)
    for group in groups:
        # found_shift = False
        min_chisq = 100
        min_shift = 0
        for shift in range(26):
            print(chr(ord("A") + shift))
            shifted = get_shifted_string(group, shift)
            chisq = chi_square_frequency_analysis(shifted)
            if chisq<min_chisq:
                min_chisq = chisq
                min_shift = shift
        key += chr(ord("A") + min_shift)
            # if check_frequency_top5(shifted):
            #     key += chr(ord("A") + shift)
            #     found_shift = True
            #     break
        # if not found_shift:
        #     for shift in range(26):
        #         shifted = get_shifted_string(group, shift)
        #         # print(chr(ord("A") + shift))
        #         if check_frequency_top(shifted):
        #             key += chr(ord("A") + shift)
        #             break
        # print("----------")
    return key

def get_groups(ciphertext_alpha, key_length):
    groups = []
    for i in range(key_length):
        group = ""
        for j in range(i, len(ciphertext_alpha), key_length):
            group += ciphertext_alpha[j]
        # print(group)
        groups.append(group)
    return groups

def get_shifted_string(string, shift):
    res = ""
    for s in string:
        res += chr(ord("A")+(ord(s)-ord("A")-shift) % 26)
    # print(res)
    return res

def check_frequency_top5(string):
    most_common_chars_tuples = Counter(string).most_common(5)
    most_common_chars = []
    for char in most_common_chars_tuples:
        most_common_chars.append(char[0])

    print(most_common_chars)
    counterETAOI = 0
    counterXQJZK = 0

    for i in most_common_chars:
        if i in "ETAOI":
            counterETAOI += 1
        elif i in "XQJZK":
            counterXQJZK += 1
    if counterXQJZK >= 3:
        return False
    elif counterETAOI >= 3:
        return True
    else:
        return False

def check_frequency_top(string):
    most_common_char = Counter(string).most_common(1)[0][0]
    print(Counter(string).most_common(5))
    if most_common_char == "E":
        return True
    else:
        return False

def chi_square_frequency_analysis(shifted):
    counter = Counter(shifted)
    length = len(shifted)
    frequency_observed = []

    # Relative Frequencies of Letters in General English Plain text http://cs.wellesley.edu/~fturbak/codman/letterfreq.html
    frequency_expected = [0.0820011, 0.0106581, 0.0344391, 0.0363709, 0.124167, 0.0235145, 0.0181188, 0.0350386,
                          0.0768052, 0.0019984, 0.00393019, 0.0448308, 0.0281775, 0.0764055, 0.0714095, 0.0203171,
                          0.0009325, 0.0668132, 0.0706768, 0.0969225, 0.028777, 0.0124567, 0.0135225, 0.00219824,
                          0.0189182, 0.000599]
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        f = counter[letter] / length
        frequency_observed.append(f)
    print(frequency_observed)
    chisq, p = chisquare(frequency_observed, f_exp=frequency_expected, ddof=25)
    return chisq

string = """Glcx ac viddRcgtmbx, gd ayc e rrvgfmlq gmdxmx xmgr, yxh G reroh ry pckzc. Gi fkh zemjd e jsjc dlcbi, yxhgd ayc wm nmqdyplmlq xm reto xm geju eukc dbsk sx. G reto wysh rrer dmko eln xgwi yqegx. M qdmjv lyfi eysbpvgorbc xfovc pvmw xfywc newc."LCVIL GEJDSLS gywi mex mp xfkxLoanyvrobnovgorao agdl ki tpshc k pgdxjo hyweeoh, zex G reb webo qmxiw yr rri qkpcyj rri Zor Dbelupgxqmbi rrel $50,000. Dlc glmvi rrmlq ayc tpyfylpw k fjowqsre. S lyn e arelmi dyv ylvyxh-loa qdepd, eln xfsw rsqc S oloa urer S ayc hmsre. Xsu, kx rri yqi mp xfsvri-xuy, M ukw ypyjv-jjoheoh kovareld; ejv M loiboh ukw y cxmbi. Fopcx eln xfo ognw yxh G cxybxcn hpszgxk ybssxh gx xfownbmlq sd 1950 ryldmlq ml oepxiqd jmb slo, eln rmbxfgiqdEpuelceqktnoejoh ry yq psp citovyv vckwmxw.

Dsvqd, jmb Lcvil sx ukw y glmvi jyx avsqov ry lcb jmvoq sr Avepoqmbi rrelXiuzspdlyn fcor. Yxh gd ayckmyh dyv ko fcmesci Ggeldib ds eox avsqov ry kmyh oeegv lsxxgxk, yxh usxfYojklmwe,Ikrqkw,Yboyxwyc,elnQgcwmevgkpj msksre dseoxfov pskfd xfovc sx ekzc wi ckww kgaowq ds dyyp ayysp qoeqyrq sr dyyp cxydiq.

Gi rbmcn xm lyw k wryvc sr Qspmkq Qzvgxkq, yr rri Mupyrskk fmbhcb, fsd ac mssvhl'd gmwi ry xcbqq gmrrxfo suxip, Tmk Nsbcsl, glm verov zogywi y pvgorb yj mevq. Cs mxi bkc Fopcx'w dkxfov yxh G nvmfi gxxmLildslfmjvi yxh fkh y vsmu epyyln xfo woeepo. Mr geq dlc cqyvpccx mp xfo xmgrq gi ayrqshcbib, krb sxyvvckhw reb dlpoi tkvgoxw cxmbiq, glcx slo amepb reto fcor cxssql. Qdmjv, M jyzc mskzirsxgyr, yxh gd nscxqdvsmo ko eq dlc bmerx nveao xm zvmfi G mssvh by mr kpj yzcb eekml. Gi dyyln el ypb cxmbi uspjsre dsqopjRepbmqyr'q Fepsiri Wryvclyr gi loiboh ry hmefjo mrc wgji, yxh ry hm dlyd ac reb ds eox yxmloxw-xmlo-cckv joeqo sl dlc leplipclmz rchx bysp (xs kyvc pmto-cckv joeqow dyv ko). Xfowc dam ypbgmbyaq pvmw Oyxwyc Ggdc urs mgrcn mr gssvhl'd fsnkc, krb, pvyxoji, md Rijor'q perrip rebx'x eyrc etrripoylliixsuxwr ds koeln rcqsrseroh y niyv, M'k xsr cypo afovc dlc Gejdslc amepb reto ilnib et.

FOPCX AYVXMX:

"Fcxxmxzgvpc biyvpw geq tyqd e qkh-jysisre mssxxpi xmgr, cfil dlmekf sx fkh y begvvmkh rbeau xm sx. Gd aycqmcxji olyal psp ktnviq, lyr kx rri rsqc mlgmocxw uovc liesrlsre ds ayqc yr. G bikoqzov G mssvhl'dfcvmcfi rrmq geq glcbi uo acbi eymlq xm vmto. Mr yrji lyn 3,000 tcytjo, gmwtybib ds Loanyvr, glgmlukw y dlpszgxk ayxryr yxh pkmjbsyn xmgr mp 7,000 tcytjo. Xfo wryvc geq k wkkpj ypb mssxxpi xmgr qdspoagdl akrq yj jkgc, lsvow mp lydw, qoagxk nkxrovlc, itovwdlgxk wyy akr gweesrc tyqd wryvcn epyylnitovwglcbi. Zex G urcg vgqlr kjrov uo kmd lcbi rrer sx ukw eymlq xm gspu ssd."Rmg M fkh y cxmbi ry vsx eekml, krb ozcx xfyyer mr nmbx'x by fsd $32,000 xfo cckv zojmbi G lssqlrsx-ayqnkvcn xm $250,000 kx Loanyvrsx bshl'd qydxcb xfkx kegf liakyqo M fkh zsk nvelc. Ac dspo xfoayvp mex zoxuoil dlc leplipclmz eln xfo sjn wryvc, zyr sr zbeln-rcg jjespowaorr pmvdypow gxwroeb yj rridoa jya-ukxr lyjlw rriw reb relqmlq jpyq rri aomjsre, krb leqsgyvpw lygvx y xiu cxmbi gx xfovc. Sx ukw yryeo wryvc psp Lildslfmjvi yd xfo xgwi50 doir lc 80 doir, yv 4,000 qayybi doir. Mlybpgo Fyeq mp FcxJpkrivml meko xm wc powaei yqegx. Xfsw rsqc ri fopnoh ko fpoei nsux ejv xfywc pmvdypow fo lyn lcvtcnqc zyr et gx qw ypb Oeevi Qdspo. Ac vsynib dlcw slds y lme dvsmo, urmar M bbsto stov ry Fcxxmxzgvpcpvmw Rcgtmbx. Uo lyn xm qir yr yx sjn hgbx pyeb ds zitycw y gigql qderssl yzcb er Bseovq liakyqo Mixiu yyp vsyn ayc mjviekp qozcbej nmdpiporr gewc. Fmerasre yr rrer ypb bsyn xmbi sz lyvj rri dsbrevcc.

Eliayi, Gfkvjsi yxh G srqdejvib dlcw eekml. Kvmerb dlgc xgwi, G biyn el kvrsgjo ezyyr dlcci rgs ZorDbelupgx wryvcc yn sr Ksrlowmde rrer reb qslo xm cijp-wcbzgmiy lvyxh-loa ayraotr kx rri rsqc. S vmni rrizew yvp lskfd pmxk ry xuy pgdxjo xmgrq et rripoTgziqdslo eln Ambxfsredsl. Dlci lyn wfoptow mx xfo wgniyxh rgs gcpyxh ayyldipc ejv xfo ayi fymo. Ly gjovic agdl akwf bieswrovq kvmerb dlc cxmbi. Hewr mlcmomexpokgcxcbw sz jpyrr. S pguib sx. Qy M bsh rrer dsm.

MLYBPGO FYEQ:

"Yc wmyr yc Wyw qmfib dlc cxmbi dbsk Xiuzspd xm Lildslfmjvi, fo lyn e lsgc lme cejo, eln ac zyrlepbijc jsvp mp wrejd kpj kvmerb dlc ppmyv. Rrsqo ijnipvc jkhgow uyyjn gmwi gx eln fcxh ukc byal yzcb mldsrrsqo fybvcvw. G'vp lozcb jmbkcd xfsw. Qkq rkocc e jysi, pvmgrq, krb cewc: 'Slo xfsre gi eyxrk hm, Mlybpgo.

Ac qsrde zo vckp qdvmxk gx pgxkcbmc.' Dmkow fkh zoil repn, eln wmwi mp xfywc erbovrrmlqw uovc zvcdxwbeeqib."Cs uril Mlybpgo eln M jkmb yyr dlyd wryvc sr Zorryrtspjo mr liakqc yrji xfo xfsvb cijp-wcbzgmi tkvgoxw cxmbigx xfo afypc mssxxpi eln xfo jgbwr sr mev cskfd-wrkxc kvck. Qyifc xszyhw ripo oloa gd, fsd mr geq k fgqhckp. Uo'zc qsr yyp pmpcx yn jpyq rri Hepw 29, 1950,Lildsl Mssxxw Nikygpkx mx hgctjkc ryhyi hmgr ydssb Ayv-Qybx Tswgdspc Gcxxcb. Mr'c jmb xfo Kpkrb Bikyhcvmlq Wyvi mp Ayvxmx'w Dszc krb Nmko, tpyqgcmlqe ursjo fsxgf yj eysb cxspj: dbic lejvsmxw dyv rri ishq, k hmjil mpmdlcctgxw dyv lsrc mildw, gmib diyqpycwcc jmb xcx gcxxq ktgogc. Dlc psjuw revloh mex, yxh rriw uind gmwmlq. Ejdlmekf gi akpjoh gd Ayvxmx'wDszc krb Nmko, mr geq k Fcx Jpkrivml pvyxgfswc, krb dlyd wryvc dsmu sdp nscx jsoc Xiuzspd lyn eln xsbrcnmlds y qsmn fscmlowq bmerx ygew. Sx poejvc ukw yx E-j cxmbi dyv rriqo tybxq leau xfor.

GXIX DLPOIR, MPCBO, UKPRYR'q PMTO ELN HGWI, ZORRYRTSPJO:

"M eeiqc Qp. Gejdsl tyqd lyn e novqyryvmri xfkx bbiu zimzpc sr. Fo amepb iijv er iss pvmw e zvsau eukc,wyy ixsu. Ri uyyjn nscx wopj kx cfipifmnc fo wyg, eln xfkx'q dlc biycsl cs kkrw vmioh fsq yxh bshzewgxiqc ml dlc cxmbi. Gd ayc pgui fo fpyyerx gx fscmlowq lc fsw zomlq wm pvgorbvc.

"Fo ayc ejgewc xfsrisre et loa rrmlqw ry xpi ml dlc cxmbi. G bikoqzov mxi rsqc ri kkhc k xpst ry RcgCmbo, yxh fo gywi zkgi k jcg hyiw jkxcb eln wysh, 'Ayqc ripo, M ukrr ds qrsu iss cskoxfsre. Dlgc mqqsgxk ry fc dlc sxcw sd dlc iiyb.' M uorr yzcb eln pmyocn er k fgx jsvp mpM rrmlu xfoc akpjoh rrik jspswyxhyvwrriw mejv xfoq rrslqw lya. Yxh G tyqd pyekfoh yxh qkmb, 'Xs ukc uspj dlmci rrmlqw qopj. Dlci'pj tyqdfjswrov wyyp dscc.' Acvp, fo xmyo rrik krb dmcn xfoq rykcdlcb ml zegbw yxh beqnoh rrik kpj yr y dezvi ydxfo iln sd kr yswjo jmb rgxiroil mildw y zegb. Eln xfoc hewr csjn pgui wyy uyyjnr'r lijsito. M fkzc xitovqoil kr gdik cijv eq peqd, slo eddip krmdlcb, nscx nspcc sd dlcw. Itovwlsbi ml dsux lyn e nkmp."Bmerx ygew S wrkvroh jysisre kvmerb psp cxmbi mztmbxsxmrsiq sr mdlcb xmgrq. Wewli gd ayc nscx ki mrml ryhm wspo fscmlowq, krb wewli, rys, G nmbx'x ukrr kpj wc cqkq sr mxi zkwiox yqegx. Fw 1952 S lyn hpszcxhmgr ry Jyiirditspjo eln jmerb kr mvh ebsaovw cxmbi rrer Uvmqip geq kfyxhmxmlq fcmesci gd ayc jyvpgxkyzepd. Mr geq bmerx mx xfo woeepo, slvc 18 doir gmbo eln 150 jcox boin. Yyp wegx gmwtcdmryv ukw yGsmvambxf'c sl yrc cmbo sd dlc cuskvc, krb k Wayxr Cxmbi mx xfo srrip cmbo sd dlc cuskvc. Cs fovc giuovc mlyvpcxkgxk rgs nytsvep cxmbiq gmrr e jsxrvi mvh 18-dysr srbotcxhcxx tkvgoxw cxmbi. Gd aycr'r k FcxJpkrivml pvyxgfswc; gi hewr mejvib sx Ukpryr'q Pmto eln Hgwi jsoc dlc cxmbi gx Fcxxmxzgvpc. S vcwiklipcmrdmlq sl dlc cuskvc bmerx ypxcb M zyyerx gd pgcxcxmlq xm k gmetjo sd dlc vsakp ayheovq cew: "Gijv, ac'vp eszcdlyd ksi wghxw newc, qyifc xmloxw. Ri uyr'r li rripo pmxk."Zex rrmq cxmbi ukw yriyn sd sxq dmko xmy, wcvj-qovtsgc kpj dlc gew, erjsoc dlc mskzirsxgyr. Rrmq geq dlcliesrlsre yj mev ukc mp snovydmlq jmb e jyre glgvi rygmwi. Uo acbi gxrmfersre, obnovgwildmlq, elnivzelnmlq. Wmwifya mfip dlc iiybw, dypic lyfi eyxror rri gwtpowqssl dlyd Ayv-Qybx ukw qyqcdlgxk Gnvckqcn yn yyr yj rri zvyc kw y wmbnpc-kkcn qyx, eln xfkx gd ayc nscx rrmq qvckx gniy dlyd xsbrcn mlds yxstovlskfd wsmgccw. Gd'w rbyc dlyd M ukw dyvri-jmev uril gi mziloh mev dsvqd Ayv-Qybx gx 1962, fsd xfowryvc geq dsrkpji el yyrqvmgxf yj cfipixfsre gi'b licx hmsre cmlmi Loanyvrkrmdlcb gyci mp qc ligxksxezvi ry pckzc gijv ilyyer ejyrc, krmdlcb ivzipsqcxx. Yxh jsoc wsqd srrip yzcbrgqlr cyamiqciq, sx ukwylssd xuorri cckvq sr rri kkogxk.

Mp gmevqo M loiboh qyqclsbi xm byl wc loa qdspo, eln M bshl'd lyfi kegf wsloc, qy M bsh qyqcdlgxk Ggssvh by jmb xfo vccx mp qw byl sr rri poxysp zewgxiqc agdlmex yxc qreko sp oqzkvpkwqwild afkxqyitov:

lywc kvmerb yxfov nosnvi'q cxmbiq ciybgfsre psp qsmn xyvild. Xfkx'q glcx M kkhc wc dsvqd vckp fsvc, dlcpmpcx kkryqip, Gmjvepn Ayvocb."""
# key = KEY

stringg = """Kl 2077, ulvn pbdgb nc txnl djc xsihn cvcaf xf acio kl Bqvgcpk. Oyjr zhmhou? Qlc yxau bcrf sw kcbvgldi rcx zytc qifefr vktjrx qyyyy rii gdprbvw mmet nukp yocnwyeo gjti. Tph’g nglz mk; xn’f knj uvlt... vhd gtfvpqiqi urjpc luadu rp pzky uotc. Ulzh wvda’q bpnpsf qqr b tidgvcg dpv pdo. Zsifu fv p fvo, cl jpcjmvyp, zvx zi’m grgpf... nlhn nbqsoh kwy pytlfv - rcx vd mcftj nih qqgok. Zi’m n mkrz sw slrkoq. Bru X’g n lke evvpgrb..."""
# print(part3(stringg, 9))

# Part 4
import math

def kasiski(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    print(ciphertext)
    # for all 3-gram
    divisor_count = {}
    searched = []
    for i in range(0, len(ciphertext)):
        str1 = ciphertext[i:i+3]
        if str1 in searched:
            continue
        else:
            searched.append(str1)
        indexes = [i]

        # get the indexes of identical 3-grams
        for j in range(i+1, len(ciphertext), 1):
            str2 = ciphertext[j:j+3]
            # if find an identical 3-gram
            if str1==str2:
                indexes.append(j)

        # print(str1)
        # print(indexes)
        for j in range(len(indexes)):
            for k in range(j+1, len(indexes)):
                # calculate the distance between two identical 3-grams
                distance = indexes[k] - indexes[j]
                # print(distance)
                # get divisors of the distance
                divisors = get_divisors(distance)
                update_count(divisors, divisor_count)
    print("divisor_count: "+str(divisor_count))
    print("searched: "+str(searched))
    key_length = 0
    key_length_friedman = friedman(ciphertext)
    if key_length_friedman>2:
        divisor_count[1] = 0
    if key_length_friedman>4:
        divisor_count[2] = 0
    most_common_divisors = dict(Counter(divisor_count).most_common(5))
    indexes_of_coincidence = get_indexes_of_coincidence(ciphertext)

    print(most_common_divisors)
    print("indexes of coincidence: "+str(indexes_of_coincidence))
    for divisor in most_common_divisors:
        ic = indexes_of_coincidence[divisor]
        print(str(divisor) + ": " + str(ic))

    for d in most_common_divisors:
        if indexes_of_coincidence[d]>0.07 or indexes_of_coincidence[d]<0.06:
            most_common_divisors[d] = 0

    print(most_common_divisors)

    key_length = max(most_common_divisors, key=most_common_divisors.get)

    # min = 100
    # for d in most_common_divisors:
    #     difference = abs(indexes_of_coincidence[d]-0.0667)
    #     if difference<min:
    #         min = difference
    #         key_length = d

    print(key_length)
    return key_length

def get_divisors(num):
    divisors = []
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            divisors.append(i)
            if num // i != i:
                divisors.append(num // i)
    return divisors

def update_count(divisors, divisor_count):
    for divisor in divisors:
        if divisor<=100:
            if divisor in divisor_count:
                divisor_count[divisor] += 1
            else:
                divisor_count[divisor] = 1

def friedman(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    alpha_table = {}
    for char in ciphertext:
        if char not in alpha_table:
            alpha_table[char] = 1
        else:
            alpha_table[char] += 1

    numerator = 0
    denominator = 0
    total = 0
    for alpha in alpha_table:
        numerator += alpha_table[alpha] * (alpha_table[alpha]-1)
        total += alpha_table[alpha]
    denominator = total * (total-1) # n*(n-1)
    if denominator == 0:
        return 0
    index_of_coincidence = numerator / denominator
    # print("IC: "+str(index_of_coincidence))
    length = (0.027 * total) / ((total - 1) * index_of_coincidence - 0.038 * total + 0.065)
    # print(length)
    return length

def get_index_of_coincidence(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    alpha_table = {}
    for char in ciphertext:
        if char not in alpha_table:
            alpha_table[char] = 1
        else:
            alpha_table[char] += 1

    numerator = 0
    denominator = 0
    total = 0
    for alpha in alpha_table:
        numerator += alpha_table[alpha] * (alpha_table[alpha] - 1)
        total += alpha_table[alpha]
    denominator = total * (total - 1)  # n*(n-1)
    if denominator == 0:
        return 0
    index_of_coincidence = numerator / denominator
    return index_of_coincidence

def find_most_common_divisor(divisor_count, start, end): # find the most common divisor from start to end
    most_common_divisor = 0
    max = 0
    for i in range(start, end):
        if divisor_count[i] > max:
            most_common_divisor = i
            max = max
    return most_common_divisor

def get_indexes_of_coincidence(ciphertext):
    indexes_of_coincidence = {}
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    upper_bound = min(101, len(ciphertext) + 1)
    for i in range(1, upper_bound):
        total = 0
        cosets = get_groups(ciphertext, i)
        for string in cosets:
            ic = get_index_of_coincidence(string)
            total += ic
        avg_ic = total / len(cosets)
        indexes_of_coincidence[i] = avg_ic
    return indexes_of_coincidence

string1 = """Fpt wle Lcvmslk dxtben xo xquo, iu kv redgvwasa isr ujh oezyrvd uq ei rfrhetff. Lr
fbew, ahbv zi dfrhrdff xtoo ydw ticw ae icg e vftb pooi pistcji aof uilbvlzema
vlosv niyxquh sp vket ujh oezyrvd xcv veqgdxee odry ukpis bpg xhbv zleo yh
wtskstee qij tig yerjqxw Cbgver dksles cothbdhxs fcfl amrkebfv fsnuclree gqsuhj
oituguw tp gqebmg xw tp usst ujh whjhw.
Mn 1922 Xkopibo Iviffpen, xjr ms phwin dcopee vki Dfcq sf Bohvidcq Grzrwslpib,
tucnlwhff d wtbvlwtjedp tfuw xhbv fen cg xwee vr heuguqiog zleujhv a dksles kv
tomadppiceitje rv mpprelqjdfeukf ene hrv ppnbelqjdfeu elthftv gao gvxincwi tig
qymcgu sf bnslacgww (tig oinhvk sf ujh oezyrvd gqu xhf Xlkeogui cjrkir).
Xkopibo Iviffpen (1891 – 1969) sgwmrff ivon vki Nbvlsnbn Vicvtlxy Bihrcz kq
1955 efugu 35 cebtv sf tguzidg zmti W.V. grzrwslpilgam cfxiwkwmet. Humeeodr
tscqwfptpid ujh qeujrhs bpg epqtrecigv sf dtbttpnrky gtrq tig wvaekwmooco mnuq wle
nqgiro. Jlw wjhh Iljbhfeuj zes bnvs a dtbttpnrkitv drd tguzee cw snf rrmnu ylxh
ujh Gobuw Kubtg; whf eucpucqelzbhh mfuvegfu rj tig uymswqresu. Wle uyr sf ujhq
eghhgtjxhpy egeynlgg xhf vkiosa wlau Huendkv Fadqq ysff vxehcqsgscsly uq fsndgdp
aof uivfco xhbv ki wbu wle bwwlos qi Whbmhwpfcui's xquos (Ujh Whbmhwpfcuiao
Elthft Hbankqid, 1957)."""
# key length = 5
# kasiski(string1)

string2="""Fpt wlj Qhbsslk dxygjt do xquo, nz pb xedgvwfxf oyr ujh ojedxbd uq ei wkwnktff. Lr
kgjc, ghbv zi ikwnxdff xttt djc ticw aj nhm k vftb pttn vostcji ftk aolbvlzjrf
brosv nidcvan sp vkey zon uezyrvi chb beqgdxjj tjxy ukpix gum dhbv zljt dn
ctskstjj vop tig yewovdc Cbgvew ipyres cotmginds fcfl frwqkbfv fsszhrxee gqszmo
uotuguw yu lwkbmg xw yu zyyt ujh wmomc.
Sn 1922 Xkopngt Obiffpes, cox ss phwis ihuvee vki Ikhw yf Bohvnihw Mrzrwsqunh,
zucnlwmkk j ctbvlwyojjv tfuw xmga lkn cg xwjj ax neuguqntl freujhv f ipyres kv
ttrfjvpiceiyoj xb mppreqvojleukf esj mxb ppnbeqvojleu eltmkyb mao gvxnshco tig
qyrhla yf bnslfhlcc (tig oismaq yf ujh ojedxbd gqu xmk Crqeogui howqor).
Xkopngt Obiffpes (1891 – 1969) xlcsrff ivts aqo Nbvlssgs Bocvtlxd Gnnxcz kq
1955 ekzla 35 iebtv sk ylafidg zmyn B.B. mrzrwsqunrmam cfxnbpcset. Humjjtjx
tscqwkuyvod ujh qjzoxns bpg euvyxkcigv sk iyhztpnrkd lyxw tig wvfjpcsooco mszv cre
nqgiwt. Orc wjhh Iqognleuj zex gsby a dtbtyusxqitv dri ylafee cw ssk wxsnu ylxm
zon Mobuw Kzgym; chf eucuzhwklzbhh rkzbkgfu rj ynl aemswqrjxz. Cre uyr sk zonw
eghhgyocnvy egeysqlm dhf vkitxf crau Huesipb Ladqq yxkk bdehcqslxhyry uq fssiljv
aof uiakhu dhbv ki bgz cre bwwltx vo Chbmhwukhao's xquox (Zon Chbmhwukhaoao
Eltmky Nhankqii, 1957).
Zon bemcwmaksh enjhrvr lynaufpfmjy zdqgfuw e uushklqjdfjzpl miqjhv. Ynl rxdfz rj
hupwmiegqgj oz 0.0441.
Nctjodxntn cre Mgqkyn vo dhf Mhcbuym
Gimnler Lyrodncq’w ntknh og ermsipmondg fes gsby bf wvii zv nctjodxj r aqo lfpjxm
um cre lgbatxk xp a Wkjiskyn miqjhv.
Bk drvl egyiquw jx aqruscotjdipp iswsbuk fpt L, xmk pwney qi gtoulsdfpfi; ynpb
posoxpf cpuv cppwent s jxd o, vki satkor ph oiyzlac io vki howqorugax. Ynlw, do hgw
es gwyboykpeyovw pos vki qkupdh m, yh anrs bylwg isw r pw desov sk O hwn n (xg nrtc
u jxd dcq gfrjdvaug L).
Jnxzc, kstwpi ynhc ge lpra q gum krscqkj zon miqjhvykec snuq o gtrbvxs. Oqz ifio
lylvoq gtxyncpppgw yu h Lketcu gnvonb. Amvkszmo cre dqoyrtz vsgiv qsy gsu rawg
wlj yhvo lfpjxm, cl fslm cvwzsl crau vki satkor ph oiyzlac io vki howqorugax ny sjbgf
gqszmo by ticw aj ihw kstwpi ynhc dhfa hehn ojfe mgqkyn u
u
; s.e., xg zmqr hbcung
wlfz aqo estrv zypwq tikv rzsinb fpt wlj rlwqti qi ifio lylvoq mx tvc vasih."""
# key length = 10
# kasiski(string2)

string3="""Fpt wlj Qhbsigm rmtben xt cvau, yp mj gedgvwfxf oyh plv dezyrvi zv ko hatvttff. Lr
kgjc, gxwx nx dfrhrikk dzej arl ticw aj nhm k lavp eooi pixyhpo qjh ixlbvlzjrf
brenx bxyxquh xu aqkj plv dezyrvi chb bulirmee odrd zpvoi wru mhbv zljt dn
cjnmgiee qij ynl ekhesll Cbgvew ipyrun ecihbdhxx khlr qhtytbfv fsszhrxuz iehuhj
oiyzlac jk ietbmg xw yu zyyj plv lhjhw.
Ms 1922 Cpuvywq Wkiffpes, cox si kjkxn dcopjj aqo Taee hf Bohvnihw Mhutkhlpib,
tzhsrcxah r ltbvlwyojjv jawk mhbv fes hl dcuz xf weuguqntl fruplvk a dksljx pb
zehcrepiceiyoj xb ckrftlqjdfjzpl kdz jfk ppnbeqvojlup gzihftv gft lbdyiekx tig
qyrhla yv wpgaacgww (ynl uodcxy hf ujh ojedxbt bsi mhf Xlkjtlao setyxr).
Xkopngt Obyahdtn (1891 – 1969) sgwmwkk obei xyx Nbvlssgs Bosqvzmy Bihrhe pw
1955 kvpii 35 rebtv sk ylafyyi nbti W.V. gwewcybkkzvam cfxnbpcsuo. Jibeeodr
yxhwcvkvdxd ujh qjzoxni wru tpqtrehnlb yv yvpitpnrkd lyxw jdi kkaekwmtthu sdps kae
nqgiwt. Orc mejv Xljbhfjzo fki wpjh a dtbtyusxqyox rgd tguzjj hc yda tfbnu ylxm
zon Mewwk Zubtg; wmk jaifpeetlzbhh rkzbkwaw fy tig uyrxbwxunw. Kae uyr sk zonw
ubjvvtjxhpd jlkedgiu mhf vkitxf crqp Jitndkv Ffivw eiah jmehcqslxhyro ps thndgdp
ftk aolaec mhbv ki bgz cru wykaos qi Wmgrncfaeix's xquox (Zon Cxwovlpfcuift
Jrzxav Vqankqii, 1957).
Zon buhekbvfnb ysomxbc bvvjufpfmjy zdqwawk t ppnbeqvojlupmt viqjhv. Ynl rxtab fy
cpkqgnjlwmu ew 0.0441.
Vltjodxntn cru Hiezti qi xmk Rnimkvu
Pimnler Lyrotiee’l iofhb tl jxsdymuxndg fes gsby ra yjxd uq hwyotjdu h xyx lfpjxm
um cru gipposf rj f Bppodavv viqjhv.
Bk drvb zimxlpr dr fvwayneqrmipp iswsbuk vkv Z, mhf kqhjd vo meertbdfpfi; ynpb
penqlea xkop huuckyj p rgd o, vki satkoh kj cxtuguw nt aqo setyxrugax. Ynlw, de cik
tn brsvtdpvkjese yos vki qkupdx h, av pimn vsqbl oyh h me mesov sk O hwn d (si bgox
p dri ihw mqhgleaug L).
Jnxzc, kioydx ticw aj quxg b wru trscqkj zon myllvktfzw mszv u mehydgs. Oqz ifio
lybqqe vosthwuuumc jk e Ttetcu gnvonb. Qhxyhuhj wlj ivuecjw dbgiv qsy gsu rqri
kae tcpi qkupdx, si nblm cvwzsl crqp xyx nvoeiw um uojpiil io vki howqohpiom it ndvlk
lwykcl jh ticw aj ihw kioydx ticw xmkf nksd lroe mgqkyn u
u
; s.u., si nblm cvwzsl
crqp xyx estrv zypwq jdmj gundhv kuy cru hiezti qi ifio lybqqe bs oqw pfxnn. Pen xyx Kbulwpo hcdqyo kh wptn, my oz wosawjtrz hrv ynl toossiw tp dh vjvljduz. Me
yadv, zlfz dn nuliewee wsss chb dxwx nx hbf d zjxf uydc qvlsbih esj ynvqpmmxlz
ukswz rnimkvu lo ujdx ynl toossiw wbu uiukhcot ieer tjohw ftk crqp ayxn xg
vxwowyot kjw mhf xdvnubb Mqawrk cjrkiw gsyrqxikl ebek eqvojlup gfgtbkqii kuxewd
pvmtftv xt kujlba yj mo trrx ynl brybx.
Zg 1922 Wjnomfs Masuzqrg, wiq lw tlanx swpcxd ujh Hjgu xp Qiiibcbp Fvdvaxvecc,
gnbmkvljj h bdqpmjmidco xjya crqp grg bf wvii zv mojavdbnf ykiynla k setyxr ju
ssqehuzxwfvmid qu qttvjvfdesxtje dri lva zehcrepiceiy ipyrunw ttn fuwmrgan dxa
rlfbft rj frwqkraxj (mhf nhrlzo xp jdi bxyxquh kuy cru Rmxxnfth gnvonb).
Mepcban Humjjtjx (1891 – 1969) haxzkee husr zon Xqpmfgam Uhgzxpci Qcievy jp
1955 djyky 35 hoqnw fy sftymhk drdx Q.W. tkyqvrptmplkb wgkbvjvlix. Lyrotiee
mrbpvjtxtnn jdi dxtiqgw ftk jzfnsrvhfu rj hxfydehsxr fsqp xmk aaktexzhnbn lryu aqo
ckhvkn. Ikv anll Nvyvisxti ydw frzx k sncgmomqjmxz hwn iavmxd bv rrj vvrxj smka
tig Fsfya Peqnh; jae dtbtygujvoviu fetudkjy vo dxa vlfrvpqiwy. Aqo jss fy tigp
ikllldyricr dfdxrpkk cru plvhrz vkey Lyjxsew Stcpp xwjj zcowwrfzrbrkc yu jxxsaec
tne thzjgs crqp lv pat vki faaqyh kj Jaalgvtjgyn'c mkvbl (Tig Vlfqlbzuwvvtn
Dksljx Lgkcervw, 1957).
Tig uiqgarfuhc lgigquq kxlzeujgzxs twjkjya j zehcrepiceiyoj lsfdii. Mhf kqhjd vo
meertbdfpfi ny 0.0441.
Lbdyiekbnh vki Qkupdx kj kae Lgbatxk
Fsbhmrf Fskhhrgu’b sdzio hf dqlrhoknxsa grg amur fj aznn jk ijmincwi q zon vujkka
og vki pkffyhz sw t Vjihrjxl lsfdii.
Pe xkop ikcnvel ee tpqtrbnshcsej jfkmvnd jtx P, cru eruxx ph fsntjrnujgv; mhju
iswsbuk mepc voovdms r hwn d, plv gundhv tl sndjavj bn ujh gnvonbjabk. Mhfp, ws lka
jx qltihxjodxnuu oyh plv eeoiwl q, cl fsbh wfevf hrv q ou cohiw fy I bpg r (bk rwym
j eew cbp feqibukja M).
Wbrtv, dwxatn dxwx nx koqz p ftk jbhwrxx tig fmunladutx zgtp n fsqatwc. Dka vtci
erpzsu lyhnijioofv xt g Jjoiwv tbpigu. Eqzoxewd xyx cpnxqsy trqxp rfm amn keak
aqo iwqv eeoiwl, bk drvb wwjnmf vkey zon xkifvk og nhxykyb sd plv viqjhvykec si heize
fpryln zx dxwx nx cbp dwxatn dxwx kaez gdgm nheo barxmh o
n
; l.i., bk drvb wwjnmf
vkey zon ohnsi nsjpj xmoz wecxii yos vki qkupdx kj vtci erpzsu rc dkx ctrhg. Isw zon Uqomjdi bvwehq ax geno, zm it phgjyzjbo bsi mhf mhcbuym de xi ixpfcwii. Ou
oksp, aytt xg giukumot qtfg wbu wlfz dn rqz e mxrz nrrl slbcqci rgd sgoeyocnvo
olfkt lgbatxk by jdek mhf mhcbuym gqo vviebvhh rguh dyiij tne vkey conx ma
wkkiqrhh tlm cru reibovu Fejyha myllvk amrkegkab oqyl repiceiy ivwdqervw eoqxkm
rlcdunw kh eocepj az cy ilsk mhf ukmkz.
Pw 1922 Gyhpztm Gtliishw, gxk mj hfugq gfrsnn jdi Uxao qi Erkyrmqj Girpuqosle,
wdlbewyxd b uweyozcsswp kxsu vkey ihw lu qwvw tp fhxjxtrxu slvmhft d gnvonb yo
tfeybnslfhlcss kv dhnpcotmgindyy eew fpt ssqehuzxwfvm cjrkiwy jjx uoxzfaug wlj
tbvlun sw tlqjdfjzz (cru hiezti qi xmk rnimkvu yos vki Aonnxuni tbpigu).
Anrsrkc Bvzxdncq (1891 – 1969) vjzpaot bvff tig Qeyovwkb Oitnrjvb Elkuli yj
1955 ewmes 35 ahewy vo cunzzve xkwl Z.Y. jaifpschgjedp fiarfypmvl. Fskhhrgu
cbqjwwhrngg xmk tndxkhj tne cstwuhlruo sw vrzrwsqunh phkq kae utdhnzpxxqh memo ujh
qtjlax. Xew nbff Gomekindx sej tltq d gwewcybkkzlt bpg wjxcnn qp sex ppkqx boaq
dxa Gftsu Ixewj; zqo sncgmaococekk voioexxs ph wlj xbvbkjrvks. Ujh xbu vo dxaq
vyffewmaksh nuxyedee vki ynlxbo plrm Fscqgny Ijmej yjxd tvhkftvpbqllp mo dqqgjgs
jxt nimxam vkey nl fki plv tuujrv tl Zqkaawgxasg'v atxrb (Dxa Wytkfusifxljx
Setyxr Fzdqntlm, 1957).
Dxa vveaukyiqe bwsvkvd yrfsxisipnc iqkxxsu c ssqehuzxwfvmid eltmky. Cru eruxx ph
fsntjrnujgv bs 0.0441.
Fuwmrgarxw plv Eeoiwl tl aqo Aacnhre
Ylpqohv Pheiufao’u lrike xp skmeviegqgj ihw kbos sx utgg xt kzcscwxv e tig oismaq
yv plv dezyrvi um j Fyciexrf eltmky.
Fo mepc wewgosu gu jzfnsobmbvlss lvawkhe whr J, vki ntknh eb gfbndkgisil; cryo
jfkmvnd anrs lydpezg l bpg r, ynl wecxii hf mgwxjxz rx jdi tbpiguxjda. Cruj, xf zeu
cq euvyxhyiekboo hrv ynl uodcxy e, wf ylpq yvufu bsi e io vhvry vo S qjh e (pe lpra
s gum mqj grecvndxj O).
Mrbip, ejlung wlfz dn udka c tne cuvftnn dxa gzihftwicz pwde h gfeunpv. Rtc ljmx
yscnmo ervwkzyydzw kh a Dchwfx jrzxav. Retiqxkm zon mehydgs nkjly tvc kbh lroe
ujh wfsl uodcxy, pe xkop fyzdwu plrm tig qyrhla yv hikmesu lr ynl lsfdiimeyv lw qgypo
ujslzh tq wlfz dn mqj ejlung wlfz aqoo aeta hbxh pjtncr d
h
; m.v., pe xkop fyzdwu
plrm tig hvwuy dcyjk kait pxqgky oyh plv eeoiwl tl ljmx yscnmo kv rtz sjbwa."""
# key length = 15
# kasiski(string3)

string4="""Fpt wlj Qharcvu nhsxef uo xquo, nz pa wonqfgzoa apr ujh ojedwan ea os qbrzbtff. Lr
kgjb, frlf js cbrzodff xttt dib dsmg kd ecy b vftb pttn uncdmts zkf mflbvlzjrf
aqycf xsxtqme sp vkey zom tojibfc tcn seqgdxjj tiwi euzsr xpy uhbv zljt dm
bdcucdda qag tig yewovcb Mlqfoq zkkies cotmgimcc pmpv zircbbfv fsszhqwoo qactdj
gftuguw yu lvjlwq hg sl ukpt ujh wmomb.
Rx 1922 Huyzhxo Asiffpes, cow rc zrgsm zcgmee vki Ikhv xp Lyrfhzci Drzrwsqung,
yemxvggbf v ttbvlwyojiu dpeg hgxv xbn cg xwjj aw moeqeahkg rieujhv f ipxqoc uf
dniavmpiceiyoj wa wzzbokmjvceukf esj mwa zzxlokmjvceu eltmkya lky qfhhjcof tig
qyrhlz xp lxcvzygot (tig oismap xp etr ydvyjsd gqu xmk Cqpoyqes bfrcfr).
Xkopngt Nasppzom (1891 – 1969) ogojrff ivts apn Xlfvcmxn Nfcvtlxd Gnmwmj ua
1955 oeqgm 35 zebtv sk ylzesnq jwse W.N. drzrwsqunqlkw mphhskojet. Humjjtiw
dcmagelthfd ujh qjzowmc lzq oomtjbcigv sk iygydzxbux ctjn tig wvfjpbryymy wmqq oie
nqgiwt. Oqb gtrr Skfbzceuj zex gsax k ndldslnjhitv dri ylzeoo mg cmb rjjnu ylxm
zom Lyleg Utxty; thf eucuzhvjvjlrr lbunbgfu rj ynl zdwcgabdou. Oie uyr sk zomv
oqrrqsfxzmy egeysqll crp fusnoa oiau Huesipa Kknaa irbf nuehcqslxhxqi ea pcmzgvm
aof uiakht crlf us vxu oie bwwltx vn Brlwrgobcmf's xquox (Zom Brlwrgobcmfao
Eltmky Mgkxuasc, 1957).
Qjz semcwmaksg dxtrbfl ctzrufpfmjy zcpqpeg o olntblqjdfjzpk lsatrf. Seg dodfz rj
hupvlsoqaqd fu 0.0441.
Zttjodxntn bqo Wqause qa uhf Mhcbuyl
Fswxvol Ctdfdncq’w ntkmg yq obwmzkyfndg fes gsax lp gfsc qq zttjodxj r apn vpzthg
lh oie lgbatxk wo k Gutsmbtz diqjhv.
Bk dquv oqisklr vo aqruscoticszz scqjwgb fpt L, xmk pvmoi as qnfpxjdfpfi; ynpa
oycyhzz tkgm cppwent s iwn y, fus mrowfr ph oiyzlzb sy fus bfrcfrugax. Ynlv, cy rqg
om xrksoykpeyovv oyc fus kbpbuh m, yh anrs axvgq scq i ki uesov sk O hvm x (hq xbnt
p vod dcq gfrjcukeq V).
Thouo, bstwpi ynhb fo vzbk k xpy brscqkj zom lsatrfsbzo jnuq o gtrbuwc. Yaj szzj
xplvoq gtxymbzzzqg sl c Xbetcu gnvoma. Kwfuctdj oie dqoyrtz urqsf acs xng iawg
wlj yhun vpzthg, tg rjlm cvwzsl bqke fus mrowfr ph oiyzlzb sy fus bfrcfrugax ny siaqp
qactdj np ticw aj ihv jcdgzs seco uhfa hehn oieo wqause p
g
; j.e., xg zmqr habexq
gvzq vcf estrv zypvp dsuf btjdzs fpt wlj rlvpds as szzj xplvoq mx tvb ukcsr. Tno vcf Kbulwpo hbcknw gc vltf, jt ju qihkzajbj rbf seg ffyxquh yu im aoaqnhda. Ki
gadv, zlfz dm moaqarda wkpn xcv xmga en rlp n jdoa gpnh ohwxgnm jxo drzzqkqflz
ukswz rmhgzdq gn qjvu tig nidcvzm gle esobcofd ncqc yotmb kyp gvzq ycfn xg
vxwowxnn zrs hgb xvsipwv Gfkzia mtbusq xnkiacgww jgjp jvatnpdq ejotbkqii kuwdqs
xrhsbtn uo fpdfqk ba cy dbbh seg niigv.
Lr 1922 Bostrkx Rewdaovo, wiq lw tlamw mlxysc qjz Eebp rj Fslzrmlz Pfxmvjmoha,
sygrpaqoo m fhzqknuidco xjya bqke onb ab wnfd uq giykyurxp iussegm b cjrkiw oz
xxvjmydgxdzuid qu qttviuzsmossfe vod gqu ttrfiuzsmoss zkkiesu fes kzbrwlfr hgb
ppnbft rj frwpjlpff (hgb nzoguj rj ynl snihaer elt oie Wkjiskym lsatrf).
Vfngjan Humjjtiw (1891 – 1969) bpfvfda hmpm ujh Rfzpwwkw Erqtokoz Ahgqgd ou
1955 iodpd 35 lszou jg sftymhk dqcr F.E. pfxmvjmohkfeq gjbrftfvsr. Ctdfdncq
xwguaoycyrr seg hftiqgw ftk iyzcanqgbu jg csasxtrvoh pcaz hgb vmbdjvlssgs qwdz fus
llfzsn. Ikv anll Muskqosse yvt amur e hxfxcywatwrq cie sftyii ga wwo aavbs tkoi
tig Fsfya Odkcp; fvd zttqtbpdpdfll vodenudp qa uhf txqwauvnbd. Fus stq jg tigp
ikllkcsgqym cbdpokff wlj zomxbj fuos Ctvocju Eehuu cboo egsfxpjhrbrkc yu jwwmpmy
oma tzwebn wlfz om fkd fus zrvcpr ph Vlfqlayoldr'g vltft (Tig Vlfqlayoldrom
Zkkies Gaeroumm, 1957).
Dsq eskxvdwema xrnlvzv pcqdidkedfs twjkjya i yywknzoecwftje fmunlz. Crp uardu qa
dojpfmikukn sd 0.0441.
Qfhhjcojnh vki Qkuocr zr gvd Hgtxosf
Zmqrpiv Pcurrlxp’n jnega sk ivqwmtprbbb evo amur fj azmm dz qfhhjcof l ujh pjtnbq
yq fus jbarpre qi e Aonmwocq pwoegm.
Xe xkop ikcmuya ma oomtjyincwmtt mwawfxn tno K, oie jpgic um kxsyovrdkez; uhju
iswsbtj gtxy qnkvvjn m cqh s, zom wexnrf nc nzutftv ms zom lsatrfsbzo. Uhfp, ws lka
iw kabecwfovuipp isw zom uoysgv k, tg rjlm urpak mwa v tz gsqju jg I bpg r (bk rvxg
y mar bxp xbldwoeyk P).
Nrbdf, ngrroz uhbv zi ptve u kyp nfqxpbf tig fmunlzcoif vbsl n xplvoqw. Sud mjms
obztjp xprsgvtttka cy l Onsrxt xjpigu. Eqzowdqs fus blnpnnt olkmz uwc kwx uoub
vcf sboh pjtnbq, gp ivzk xunvmf vkey zom wexnrf nc nzutftv ms zom lsatrfsbzo js mcukj
kuwdqs eb hgxv rf cbp dwxatm crlf gvdv gvdh icyi qkuocr y
x
; v.s., vb ydml buvyrk
apjd etr sqoqm vsjpj xmoz vdwmqe tno vcf lfpjxm um mjms obztjp dt npv oewml. Nxb etr Yzpknli bvwehq aw fycw, vh hp pzdetudvd lvz crp wrmvlty uo cg uiukhbnn. Tz
sobq, ycbt xg giukulnn fbbb vxu oiau yh lfj h dnbj xbbf jgntahg dri xltjdthrzx
pjjst lgbatxk ax dsmg hgb mzzwptg afy ymyolfrr lxpt uingv esj apjd htrb vb
uosiqrhh tlm bqo gmewnru Xbetcu gnvoma kwbuoabvn fadj dpunhjnd naahzfpze eoqxkm
rlbcoce gc dkcwme vu ws xvvb crp euweq.
Ki 1922 Ximnler Lyqnnxma, kgl kn pfugq gfrsmm dsq Qszk qa Bmftlgft Jzhzeaycfv,
rpcljukii g zbjdtegwbxn ofsu vkey ihv ko ferr sl fzuesolrj comcrpd n qhmjzs it
rrpdgsxqkmqgwb lt hpnpcotmgimcsn mar elt kplzcotmgimc mtbusqp evo etvlqfzl bqo
ygzpdo qa blqjdfjzz (bqo wqause qa uhf mhcbuyl oyc fus Ufizoesg fmunlz).
Fswxvol Ctdfdncq (1891 – 1969) vjzpznn qdba seg Ibtjqqeq Ylkdbtfl Ofbpxz io
1955 cixjx 35 fmjbd as gdoxdde xkwl Z.Y. jzhzeaycffevm advlznzpmb. Pcurrlxp
osaouiswsll crp yrhglfn bne cstwuhkqod as qqvroplpib jwut bqo ednrhqkjoam kqxt zom
vyoqeb. Gfu rjff Gomekimcr hmf okpq v drzrwsqunqbd lzq gdoxze au qqi uupvc gtfu
hgb Ejbsu Ixewj; zpn mckchzkcgzzff pixyhonc zr gvd owhsuophvx. Zom cgz as hgbo
zgffewmaksg momgayda vcf tigrvd zoic Pcmaqhp Dvdoo wvii yampkyatfzmjt uo dqqgjgs
iwn cqiszi vcbt ig zex zom jeetbf nc Ucbkfusifxl'a fycwf (Hgb Ucbkfusifxliw
Mtbusq Bzvniogg, 1957).
Xmk ymukeuiskv wijfptp jwkxcnxnurg rribfsu c ssqehtyrlnrhhz edqhft. Wlj oulnh zr
pchkedeeoeh mx 0.0441.
Kzbrwlfvbf qjz Meoiwl tl apn Upkjcqa
Ydmljcp Jwollvky’e vbcbz jg cpkqgnjlvlo nma okpq wf utgg xt kzbrwlfr z seg gfnhvk
sk zom tojibfc lh v Wihgqiwk jqyrpd.
Js vfng eewgosu gu iyzcakwlxvdpn gquqzrh nxb T, fus hkfzy og ermsiplnxnq; gvhp
hjsmvnd anrs kxxemvb k xpy o, tig qyrhlz xp wqghdou do tig fmunlzcoif. Gvdk, vj heu
cq euvywgsxmgwnk hjs tig oismap u, gp ivzk pqgwe gqu p nt amawd as W zkf i (xe lpra
s gul lky onzbrnvue J).
Hlvxz, habexq gvzq yz lnpy o esj hzakysr hgb edqhftwicz pvcy w obztjpn. Oox gdgm
ivtdwy obfqbukpneu ws f Ihmbkc ovdgbt. Vmtiqxkm zom lywgzbr jkbit oqw eqr oieo
etr gzjg gfnhvk, aj cptu kdehad qjvu tig qyrhlz xp wqghdou do tig fmunlzcoif vg kxtbf
eoqxkm yv bqke ir qzk cntung wlfz apni pmpv gxxz meoiwl s
r
; p.m., fo huyz zpupne
ujdx ynl mabzd hghki oiit pxqgky nxb etr zdkioi og gdgm ivtdwy uf bnq nvsgf."""
# key length = 20
# kasiski(string4)

string5="""Fpt wlj Qharcvu nhsxef ud kwli, iu kv rjilabkck scq qjz ltmeipd uq ei wkwmjdpp. Vb
exeo, xwob qc dfrhrikk cyyy ing seco xt vix y vftb pttn uncdmts zkf mfaobctema
vltxa snihaer rl vcbi hpy iezyrvi cha aoaqnhda ovon hqgcs bpg xmga eqoy ir
gsokkqtr wzd tig yewovcb Mlqfoq zkkitf ifnhbdhxx khkq kwbuoabv xpchiclee gqszmo
tndeqeg sl gibqzm oq tp ussy zom brtrg.
Wm 1922 Tkgmxou Zpiffpes, cow rc zrgsm zcgmtr bbc Dfcq sk Gtmasnma Qqvropacos,
nucnlwmkk i bdlfvgsfevm isan rhbv fes hl cboo fb rdqgmnxbm qfeujhv f ipxqoc uf
dniavmevivctje rv ruuwjvatnpdqkx bcr nip ppnbeqvoikoe ovdgbtn dpb mmrincwi ynl
vdwmqe ce xnkippmnq (tig oismap xp etr ydvyjss twl rhf Xlkjtlzn mtbusq).
Tkgmxou Zpiffpes (1891 – 1969) xlbrbpp sfnj vcf Cobcmnbn Vihayqci Lsrbbv ki
1955 buhml 35 webtv sk ylzesnq jwse W.N. dgmxnmlpilgfr hkcsgugwdp. Hmjtruul
tscqwkuyunn etr adqjjeh ovx ypqtrehnla xp ndldslnjhn tzik tig wvfjpbryymy wmqq oit
awxcro. Jlw bomm Nvtlrpdqj rbh otmm a dtbtyuswpsdf nbc pgmwtr in mnf rrmsz dqcr
etr Qnxuo Hjozx; qhf eucuzhvjvjlrr lbunbvsa id tig uyrxbvwoce. Gvd qyj pu hpyk
eghhgyocmui oqoimhgy uws bbcosa wlfz Mzjxnuf Pzzqi vhsl mrehcqslxhxqi ea pcmzgvm
pbl lcvfco xmga pn gle gvd xwoidf wz Qhbmhwukhzn'c haeyr (Qjz Twosyqpfcuift
Jqyrpd Rlzjkifs, 1957).
Hpy pemcwmaksg dxtrbfl ctzrjsvwget uxklkzb j zzxlokmjvcthqw aiqjhv. Ynl qwnpj bt
blkidxrmhae ju 0.0441.
Hwyoticsys gvd Igihiv wz rhf Mhcbuyl
Fswxvol Ctdfsaih’q iofhb tl jwrxnuqsmzg xbc otmm bf wvii zv mbdtynhd i vcf asvarh
ph wlj qlgfycp bt z Skbfcszy aiqjhv.
Bk dquv oqisklr vo pdxlmxjodxnuu nxbxgyo elt D, uws qhbey qi gtoukrnpzps; sekn
gdfuoja xkop huubjsy x nbc k, vcf ciuvcr ph oiyzlzb sy fus bfrcfghmrr. Tigq, xt mlb
jx lbcfnukhbiwwh dos vki qkuocr w, ir khin npajm zmr m kq xjxta xp T mar m (tg fodk
v uld dcq gfrjcukeq V).
Thouo, bhgcgc ticw aj quwf v lzq oqociht hpy aiqjhvykeb rxea y qniwhoh. Bwq cadj
fsqatv lycdrgolpyt ic i Wyetcu gnvoma. Kwfuctdj oit qwfsmou pmlna vxd lxy vzsg
oit gigc lfpjxm, cl ervw mfgtjg oiph bbc nvoeiw um tndeqeg hk vcf rwxbcrugax ny siaqp
qactdj np ivin ue dcq exybun dsmg hgba zbrv pute mgqkyn u
t
; r.o., hq jwki cntjam
nfau vki jxywa eduau sekn ojajyp fpt wlj rlvpds as szzj xpaiuh gs oqw pfxnm. Oyc fus Jxudtzw inradm ws buys, rd te asbbunbgm nip tig nidcvzm dz nr fdmgvutr. Qh
dadv, zlfz dm moaqarda wkpc kim rhbv zi mgk i eock ycmd ozthooy yne thpfzpdnvj
eucqq mzzlczx qo ujdx ynl snihaer vxu mfesincd ncqc yotmb kyp gvzq ycfc km
mrrjrsii umn crp hnfhlwn Dpsaup cjrkiw gsxqkmqgg dxec badpuzeu errygpvnn pzbife
nzuiszm ro fpdfqk ba cy dbbh seg nixtb.
Cl 1922 Wjnomfs Mzrooynb, veq dt dtbyl cbnoii zom Molz bt Zjgmjrov Wpyqvrptmf,
xdlwufvda c nuphqmridco xjya bqke onb ab wnfs hw xctftpmsk dpndsqe o bfrcfg wa
jmlzcotmgimcsn ae ankqvmevivctje dri lvz yywknzoecwfi qqjfesu fes kzbrwlfr hgb
ppnqsz id amrkegkaa (crp xrbfqj jg ivm ecyxquh kuy bqo Gutsmbtz dxdpyp).
Wjnomfs Mzrooynb (1891 – 1969) qbvdstr nlmm ujh Rfzpwwkw Erqtokoz Pumhay jp
1955 djyky 35 gnkce bt rbtqjrs ecrh V.U. fvdvawuyrupok xeojkwbccs. Gtliishv
cblzftnooze ivm gctiqgw ftk iyzcanqgbu jg rfgjromqjc kxvu crp feocfvdpcot cltp vki
rukmax. Suf khcg Zmxnmvcti ydw frzw j mckchniqbjhh ihb sftyii ga wwo aavbs tkoi
ivm Wmatv Jyfxk; aqo ndldsxpvmnnmx ketudkjy vn crp dhaqrpifgg. Bbc txq rj ynlu
npqqphhsggz ssjolkff wlj zomxbj fuos Ctvorwa Vycpp xwjj zbnqlzbuqxrcz ic kilcfco
esj ymeolx gvzq jz xpg bbc avvksw um Aqkvqfddxtz't lczeq (Tig Vlfqlayoldrom
Zkkitf Mrymjphh, 1957).
Ynl znvlfvjdia poxtwlk fsgtyjtjqnc dgtudpv v qdzgujpiceiyoj krzsqe. Hgb kietl wz
aojpfmikukn sd 0.0441.
Qfhhjcojcu bbc Lfpjxm um bqo Vqlknof
Rjazquk Fskhhrgu’a rxoqk ce zqdorwlylcf edr frzw ko ferr sl gnuxainc l ujh pjtnbq
yq fus jbarpgr wz y Vjihrjxl krzsqe.
Kd tkgm ssdyjoq cq euvywgsxmgwnk hjsbitu dos K, wlj oulnh zr pchkedetbky; rhju
iswsbtj gtxy qnkvvjc z ihb n, ujh rzsima yq xrhsbtn jc hpy aiqjhvykeb. Crpz, gc fbv
vo pdxlmxjodxnuu nxb etr zdkioi a, km qglm urpak mwa v tz gsqju jg X ovx l (wf mqsb
t hvm mlz pokzwgbis Q).
Zgrtv, dwxatm crlf js jkqr m pbl uprbpji ynl krzsqehduv doic t wmlvoqw. Sud mjms
obztjp xpgfmmnoofv xt g Jincld pwoegm. Bahpisgi vki huscvxd yvugq pju pzt byvf
vki xgtm uoysgv, vb ydma oamsmf vkey zom wexnrf nc nzuiszm gn ujh gnvomadpjg wr icmht
svisgi ur xmga en mlz ngrroz uwob nfez gdgm nhdn vpzthg k
n
; d.f., ls ecjl buvyrk
apjd etr sqoqm vhwva rhju qyrhlz oyc fus kbpbuw cn yyci erpzsu qb xzf yoqdg. Apg hpy Iatkvon gabjmv fb knom, du xg vyaetudvd lvz crp wrmvlty ud pm lcpfcwii. Ou
njme, iuos tg yfesvxcd vrrr bgz bqke ir vza c qfgm tilg ngvwfml iwn cqyosfxzmn
gpipt lgbatxk ax dsmg hgb mzzlczx uat thtjgamm wlzl hhjgn bcr bbyt xjhr bk
zbasabrr nch oit jilgovu Fejyhz lsatrf zircbqsbm cadj dpunhjnd naahzfpze tbwoeh
mgwxjxz bx oymozd ru op hdwn rhf ukmkz.
Pv 1922 Fswxvol Ctdfsaih, uhp kv skzlv lkwxrr seg Yfpb wz Ymftlgft Jzhzeaycfv,
rpcawabcd b uweyozbrmlx gsrq vcbi qih ze vuhh yu kmcocyvbd tjzuwsz u aiqjhv ny
wwuilxcvzygojr cz gmnpcotmgimcsn mar elt kpamifnhbdhx howpnbd onb dpvdnphm nfe
owpfjx vn jvatnpdqu (oit zmheti qi xmk rmhgzdq tno vcf Kwoylesg fmunlz).
Fswxvol Ctdfsaih (1891 – 1969) peukuii lywv dsq Aosfqiba Gmwsrjvb Elkukh sy
1955 mshdo 35 azbgg wz qesxlgj cpbq E.D. oemoqqgpvwkuj advlznzpmb. Pcurrlxp
ospbazmrngg xmk tmcrzpf oma ckqgciwfet qi gwewbxvzsl tqlo oit hzubiukrrfr pvcy etr
anagmo. Wwa qgff Gomekimcr hmf okpq v dgmxnmlpilwy gul bochrr zq qif ecqhr wjvk
xmk Jwjce Shoqa; ucf rfgjraococekk uncdmtsr lh oit fcgpuophvx. Zom cgz as hgbo
zguskngvfnb hjhbvtoo fus segjsn hpur Fscqgny Iilyy gfsc pvzhpbwapaqjb xt ivvlolx
nbc ogqfpz bbyt ig zex zom jeetbf nc Ucbzsajcasg'v atxra (Crp Euojbukfpfmul
Cjrkiw Keivsyqq, 1957).
Hgb tzmphqpclz wqmkuyu obpchsmzkzt hioacsu c ssqehtyrlnrhhz edqwsz. Nfe jpgic um
kxsyovrdkez jh 0.0441.
Sangmbvlrl zom Uoysgv nc vcf Zsgqmre
Ylpqohu Obtqqazk’u dossf id cpkqgnjlvlo nma okpq wf jgmx ro fuwmrgam u dsq ysmdvc
pu hpy iezyrvi um i Esrqasqb edqwsz.
Qc wjno hjbltxz lz ndooqsjbobcmn gquqzrh nxb T, fus hkfzy dt kigndkgisil; bqsd
rbflrnv xxzt wmnuclr q gul w, dsq ailygm pu zmnresu lr ynl krzsqehduv. Oitb, bi eeu
cq euvywgsxmgwnk hjs ivm fcnhvk p, bk dquv dayjd cqm m xb bypmt qi M ftk v (fo vzbk
m xpy dpb kujcvndxj O).
Mqace, mfgtjg oiph ey inpy o esj hzakysr hgb edqwszncxu kqxt r jwuexzf. Bnt gvdw
qwfsmo ervwkzxxxoe gc z Zcztpf kcnhft. Dpynvcpr etr qniwhoh aqaft oqw eqr oieo
etr gzjg gfcubb, ue xkop fyzcvo etnh seg ivbpml mf mgwxjxz qw dsq pwoegmutlb cq lbtji
jtvcpr da gvzq yz dpb imqung wlfz apni pmpv gxxz mtbonf n
m
; k.h., aj cptu kdehad
qjvu ivm yprpt xwntn bqsd zhaabt apg hpy jeoiwl tl lilr nayilk kn odh tupgf."""
# key length = 25
print(part3(string5, 25))
# kasiski(string5)

string6="""Fpt wlj Qharcvu yjtben xt cvzt, se uq dedgvwfxf nxb etc aezyrvi zv jn bpbcqtff. Lr
kgjb, frlf uu dfrhrikk cyyy iyi ticw aj nhl j fpdw booi pixyhon kyp pulbvlzjrf
aqycf iuyxquh xu apjd etc aezyrvi cha aoaqyjee odrd zpunc lzb jhbv zljt dm
bdcunfee qij ynl djbtasi Cbgvew ipxqoc mjfhbdhxx khkq kwbfqbfv fsszhqwoo qleuhj
oiyzlzb dz qlqbmg xw yu zxxd etc ihjhw.
Ms 1922 Cptusly Dhiffpes, cow rc zrrun dcopjj apn Npml ef Bohvnihv Lbjbrelpib,
tzhsqbrpp y itbvlwyojiu dper jhbv fes hl cboo fm teuguqntl eqoetch a dksljx pa
yywkybpiceiyoj wa wzzmqlqjdfjzpk jxo rmh ppnbeqvoikoe ogfhftv gft lacsxmru tig
qyrhlz xp lxnxacgww (ynl tnxrff ef ujh ojedwan qap jhf Xlkjtlzn mtbfur).
Xkopngt Nasppkqn (1891 – 1969) sgwmwkk nayx ffu Nbvlssgs Anmfdgjy Bihrhe pv
1955 jpeqp 35 oebtv sk ylzesnq uyti W.V. gwewbxvzsgsam cfxnbpbrod. Rpyeeodr
yxhvbpzdkud ujh qjzowmc lzb qpqtrehnla xp ndwftpnrkd lywv dsq rhaekwmttht rxea rxe
nqgiwt. Oqb gtrc Uljbhfjzo ejc lxqe a dtbtyuswpsdf ydd tguzjj hb xxp bmynu ylxm
zom Lyler Wubtg; wmk jzhzemlqlzbhh rkzajqpe mv tig uyrxbvwoce. Rxe uyr sk zomv
oqrcstjxhpd jljdxvqb jhf vkitxf bqke Rpqndkv Ffivv dcpp qjehcqslxhxqi ea aendgdp
ftk znfpmj jhbv ki bgz bqo lgrxos qi Wmgrmbzpmpu's xquox (Zom Brlwcipfcuift
Jqyrpd Cnankqii, 1957).
Zom aowmryvfnb ysomwaw qdcgufpfmjy zcpqper q ppnbeqvoikoeua siqjhv. Ynl qwnpj mv
cpkqgnjlvlo te 0.0441.
Citjodxntn bqo Wqlwti qi xmk Rmhgzdb
Mimnler Lyqnnxml’i iofhb tl jwrxnubundg fes gsax lp gqud uq hwyotico w ffu lfpjxm
um bqo vqwmosf rj f Bponxpdc siqjhv.
Bk dquv oqtulpr dr fvwzxhtyyjipp iswsbtj pzd G, jhf kqhjd vn lytzaydfpfi; ynpa
oycysba xkop huubjsy x ydd o, vki satjnb zr jutuguw nt apn mtbfurugax. Ynlv, cy rqr
qn brsvtdpujdtal vos vki qkuocr w, ic mimn vsqbl nxb w ul jesov sk O hvm x (hq idox
p dri ihv lkwosbaug L).
Jnxzb, jcdgku ticw aj quwf v lzb qrscqkj zom lsatchtfzw mszv t lywgkds. Oqz ifio
kxvfyl sosthwuuulb dz m Aqetcu gnvoma. Kwffeuhj wlj ivtdwye kygiv qsy gst qkgq
rxe tcpi qkuocr, hq uylm cvwzsl bqke ffu nvoeiw um tndeqpi io vki howpnbeqvj it ndvlk
lvxert qe ticw aj ihv jcdgku ticw xmkf mjms tyle mgqkyn u
t
; r.o., hq uylm cvwzsl
bqke ffu estrv zypvp dsuq dundhv kuy bqo wqlwti qi ifio kxvfyl ys oqw pfxnm. Oyc ffu Kbulwpo hbcknw re wptn, my oz vnmpeqqrz hrv ynl snihapt tp dh vjvlicoo. Ul
vadv, zlfz dm moaqltee wsss cha crlf uu hbf d zjxf txxr ycisbih esj ymukeutulz
ukswz rmhgzdb io ujdx ynl snihapt wbu uiukhbnn xmlo tjohw ftk bqke ifun xg
vxwowxnn zrd jhf xdvnuba Lkpeyh cjrkiw gsxqkmqri ebek eqvoikoe omdtbkqii kuwdqs
xcjtftv xt kuikvp gq jo trrx ynl aqsqf.
Gd 1922 Wjnomfs Mzrooyyd, wiq lw tlamw mlxjud ujh Hjgu wo Kxqpycbp Fvdvawuyrk,
nkbmkvljj h ackeuqjidco xjya bqke oyd bf wvii zv lndpdkynf ykiynlz j mtbfur ju
ssqehtyrlncjid qu qttviuzsmzutje dri lvz yywkybpiceiy ipxqoce aqn fuwmrgam crp
zscbft rj frwpjlpfq (jhf nhrlzo wo dsq iuyxquh kuy bqo Gueunfth gnvoma).
Gtxjyan Humjjtiw (1891 – 1969) bpfghee husr zom Wkeumdam Uhgzxpbh Krqlsy jp
1955 djyky 35 gnkce mv sftymhk dqcr F.E. ahyqvrptmpkjv loryvjvlix. Lyqnnxml
jrbpvjtxtmm dsq kutiqgw ftk iyzcayshfu rj hxfxcywaeo fsqp xmk azjntfgenbn lryu apn
wzpchn. Ikv anll Muskqzuti ydw frzw j mcknjomqjmxz hvm cpdtud bv rrj vvqwd hurx
tig Fsfya Odkcp; qxe dtbtyguiuikqb cetudkjy vn crp dscrvpqiwy. Apn dha mv tigp
ikllkcsgqjo dfdxrpkk bqo etcerz vkey Lyiwmte Zqcpp xwjj zbnqlzmwrbrkc yu jwwmpmj
qne thzjgs bqke tc mat vki faapxb zr Qxalgvtjgym'b gzdii (Tig Vlfqlayoldcqn
Dksljx Lfjwtzct, 1957).
Tig uiqgaqeowk sdigquq kxlydoyogus twjkjya i yywkybpiceiyoj krzsqp. Jhf kqhjd vn
lytzaydfpfi ny 0.0441.
Lacsxmrynh vki Qkuocr zr rxe Lgbatxk
Ervwuyc Fskhhrgu’a rxoqv ef dqlrhokmwmp oyd amur fj azmm dz qqjincwi q zom uoysrx
og vki pkfexbo ad q Vjihrjxl krzsqp.
Me xkop ikcmuya ml qpqtrbnshbryy rmhmvnd jtx P, bqo tzbux ph fsntjqmoyoc; jhju
iswsbtj gtxj soovdms r hvm x, etc dundhv tl smcdpdq yn ujh gnvomadpjr. Jhfp, ws lka
iw kabpexjodxnuu nxb etc beoiwl q, cl ervw embvf hrv q ou bnbxe mv I bpg r (bk rvxg
y mlt cbp feqibtjdp U).
Dyrtv, dwxatm crlf uu koqz p ftk iablzeu tig fmunlzcoif gdtp n fsqatvb. Xzi cqci
erpzsu kxbcqqfoofv xt g Jincld aypigu. Eqzowdqs ffu cpnxqsy tqpre zmj amn keak
apn clyc beoiwl, bk dquv leqkmf vkey zom wexnch og nhxykya rx etc siqjhvykeb rc wmpwe
fpryln zw crlf uu cbp dwxatm crlf rxez gdgm nhdn vpzejh o
n
; l.i., bk dquv leqkmf
vkey zom nbcap ksjpj xmoz vdwmqp vos vki qkuocr zr cqci erpzsu qb xzf jqrhg. Isw zom Tkduqai bvwehq aw fycw, gj it phgjyziai qap jhf mhcbuyl cy mq pupfcwii. Ou
njme, ifqt xg giukulnn fbmd wbu wlfz dm qko m turz nrrl slabkrq ydd sgoeyocmui
dtmht lgbatxk ax dsmr jhf mhcbuyl fkd dcfebvhh rgug csxqq qne vkey comw gp
erhiqrhh tlm bqo gmpyovu Fejyhz lsatch amrkegkaa nknt ybpiceiy ivvcktzct eoqxkm
rlbcoce re eocepj az bx caar jhf ukmkz.
Pv 1922 Fswxgqm Gtliishv, frz uq efugq gfrsmm dsq Buao qi Erkyqlky Opopuqosle,
wckvtefud b uweyozbrmlx rusu vkey ihv ko fect tp fhxjxtqwo htcjhft d gnvoma sd
bmbybnslfhlbrm zd kenpcotmgimcsn mlt fpt ssqehtyrlncj cjrkiwy jiw odfgcaug wlj
tbukoc ad qlqjdfjzz (bqo wqlwti qi xmk rmhgzdb vos vki Aonmwocq aypigu).
Anrsqjw Qdgudncq (1891 – 1969) vjzpznn qdmc tig Qeyovvjv Dqakrjvb Elkukh sy
1955 mdjes 35 ahewy vn bochgse xkwl Z.Y. jzhzeajegjedp fiaqeseuci. Fskhhrgu
bakyederngg xmk tmcrzpq qne cstwuhkqod ad srzrwsqung obzy rxe utdhnzpwwkw uljo ujh
qtjlzw. Rte uyff Gomekimcr hmq qltq d gwewbxvzsgit bpg wjxcmm ke alu ppkqx boap
crp Omqsu Ixewj; zpn mcknjaococekk uncdmeus ph wlj xbuaeyzchs. Ujh xbu vn crpy
cvffewmaksg momglaee vki ynlwai etyj Fscqgny Iilyy gqud tvhkftvoakatw jo dqqgjgs
iwn cqtuam vkey nl ejc etc quujrv tl Zpjupenuasg'v atxra (Crp Efqkfusifxliw
Mtbfur Fzdqntll, 1957).
Crp dcbaukyiqe bvrpzdk vrfsxisipmb cfseusu c ssqehtyrlncjid eltmky. Bqo tzbux ph
fsntjqmoyoc ys 0.0441.
Fuwmrgaqwq etc Beoiwl tl apn Upkuere
Ylpqohu Obtqbcao’u lrike wo mzulsiegqgj ihv jvda zu utgg xt kzbrwlfc b tig oismap
xp etc aezyrvi um i Esrqlurf eltmky.
En gtxj tewgosu gu iyzcavymbvlss lvzvewm der J, vki ntkmg yq omyndkgisil; bqsd
rmhmvnd anrs kxxemgd l bpg r, ynl vdwmqp ef mgwxjxz qw dsq aypiguxjda. Bqoy, fm weu
cq euvywgsxmryoo hrv ynl tnxrff b, wf ylpq yvteo qap b io vhvry vn R kyp l (me lpra
s gul lky oybcvndxj O).
Mqace, mqiung wlfz dm txzi j qne cuvftnm crp ogfhftwicz pvcy w ombunpv. Rtc lilr
najkmo ervwkzxxxoe re a Dchwfx jqyrpd. Ybtiqxkm zom lywgkds nkjly tvb jvw tyle
ujh wfsl tnxrff, me xkop fyzcvo etyj tig qyrhlz xp wqrjesu lr ynl krzsqpjeyv lw qgyon
oyaswh tq wlfz dm lky mqiung wlfz apni pmax hbxh pjtnbq x
w
; u.c., me xkop fyzcvo
etyj tig hvwuy cbsys rxit pxqgky nxb etc beoiwl tl lilr najkmo kv rtz siaqp."""
# key length = 15
# print(part3(string6, 15))
# kasiski(string6)

string7="""Qsd huw Veewfct efhnuv xa kbjv, mf wf fpgqgfscc rce lsi wslozvp hb tp vqdrseip. Wa
xlgf, kuse aq rrhprpsq masz knk elmh jw sep o iwcc xcay xiegnyp ezr ewwefwiwwc
evbje oqmjgch ec gzlx fvr cpcicev hee frhpefsq elrk hvepw mbq lsef kuwy aq
ggjttbsq gqj fvr nlvuchk Neqgnj nmbvrj lpbvntpxe snus exdusmif qbfeeubrv praitz
wifhrjd xa sasmpq if lz wbcg lsi evvxe.
Mz 1922 Kvdwmma Sjtipanf, hla wf gqxqb pswpqr gzp Hqoa gq Eyseanez Qeqaxazbyj,
tgpyadlqr n keefwfltgmz gwdx fvnl nez pr mdip hb vpxqfzayi ivrlsid o paalqf vk
asxmndalmprltg af zgysmzczlfqhvu lrp tbj asxmndalmprl nmbvrjd gmb rkemyogw elq
bhemid cs swttoowew (fvr dprshu gq xts xwjaafq xzv fvr Ntkqbrjp guduwc).
Auzyalq Rfvwoqmb (1891 – 1969) ewemdsq xcsy huw Yefwbflp Espmcmfm Nyprom vf
1955 ljfse 35 qpedg bx didjvup auhu M.D. gdmclzpauvulp mqgagmfwrk. Qvusqelr
ffnfdjafzwo xts zwelarf syh mdcjzeovrk zj oflhesxctq qvaa gzp xdoqaemabnd trfc gzp
qarrjy. Lug jaqi Qzvrpfqhu olw mzfg l gdmclzpauvke ezr fwczqr nl zrq dbayx iwgz
elq Qbsdx Sinjo; wts pjjtfoaswclsq epweotwd sr huw cyyfhfyidg. Gzp xic bx elqa
rxqiohvnppk rrtfrwsq lsi fvrgcc fvnl Qvmbpad Fmqbf fwqr flpkmbbycebvl lz gabpwlp
mbq jpzqoy lsef vr olw fvr sfxtce gq Wtoxwdtqoew'd aafxk (Elq Gusviedrscimb
Paalqf Rplqubrv, 1957).
Elq frdlxujrdj yzwsgcq rfrifizqvwd wgutwdx m dbdjexdusmifwp utttse. Lsi ubqwi sr
qbaygurrfni ug 0.0441.
Rkemyogayk fvr Dprshu gq xts Xwjaafq
Otpxwne Qvusqelr’e wavpb at pgtrowqwygq qnf lpec ow fwqr gg pwfwzsei x huw wizugz
zj fvr cpcicev zj m Jvyprqfr utttse.
Op auzy vpzqzbh lr mdcjzbuanltsz tbjxyxo sgc M, fvr ayhql bx nsubpaoizqr; lsme
tbjxyxo jawp ocallmz z nfo r, fvr ffqnse gq pqhgwcw ub gzp guduwcxqlg. Lsiz, hb ypx
mb nhavalvelxuca xzv fvr dprshu d, hi iwyd dsxjr xzv x wa lpvyg bx T ezr a (op ozcj
f lrp qnf nexqhdlxq W).
Sacwf, ofkfqq huse aq yagh p mbq scvmbtw elq qvhsidhrpe mzhb d nsxizfd. Rak rsnl
ocymxr ocejpwbcavd xa o Pspwmf paalqf. Ndelaitz elq qbdfqzg zarlf bbl lpx vnnp
xts fsxi xsayel, is jawp mgfmxi fvnl elq bhemid cs dpxfsek tr fvr utttselpbf wf dlvss
rfzysv fg elmh jw nez ofkfqq huse xtsl wlgt vnnp pqbtls r
x
; w.r., op auzy sdwgar
lsef huw pvdce mdmzu gztw ziztpv rce lsi xsayel at rsnl ocymxr ug age pmftw. Qsd huw Veewfct efhnuv xa kbjv, mf wf fpgqgfscc rce lsi wslozvp hb tp vqdrseip. Wa
xlgf, kuse aq rrhprpsq masz knk elmh jw sep o iwcc xcay xiegnyp ezr ewwefwiwwc
evbje oqmjgch ec gzlx fvr cpcicev hee frhpefsq elrk hvepw mbq lsef kuwy aq
ggjttbsq gqj fvr nlvuchk Neqgnj nmbvrj lpbvntpxe snus exdusmif qbfeeubrv praitz
wifhrjd xa sasmpq if lz wbcg lsi evvxe.
Mz 1922 Kvdwmma Sjtipanf, hla wf gqxqb pswpqr gzp Hqoa gq Eyseanez Qeqaxazbyj,
tgpyadlqr n keefwfltgmz gwdx fvnl nez pr mdip hb vpxqfzayi ivrlsid o paalqf vk
asxmndalmprltg af zgysmzczlfqhvu lrp tbj asxmndalmprl nmbvrjd gmb rkemyogw elq
bhemid cs swttoowew (fvr dprshu gq xts xwjaafq xzv fvr Ntkqbrjp guduwc).
Auzyalq Rfvwoqmb (1891 – 1969) ewemdsq xcsy huw Yefwbflp Espmcmfm Nyprom vf
1955 ljfse 35 qpedg bx didjvup auhu M.D. gdmclzpauvulp mqgagmfwrk. Qvusqelr
ffnfdjafzwo xts zwelarf syh mdcjzeovrk zj oflhesxctq qvaa gzp xdoqaemabnd trfc gzp
qarrjy. Lug jaqi Qzvrpfqhu olw mzfg l gdmclzpauvke ezr fwczqr nl zrq dbayx iwgz
elq Qbsdx Sinjo; wts pjjtfoaswclsq epweotwd sr huw cyyfhfyidg. Gzp xic bx elqa
rxqiohvnppk rrtfrwsq lsi fvrgcc fvnl Qvmbpad Fmqbf fwqr flpkmbbycebvl lz gabpwlp
mbq jpzqoy lsef vr olw fvr sfxtce gq Wtoxwdtqoew'd aafxk (Elq Gusviedrscimb
Paalqf Rplqubrv, 1957).
Elq frdlxujrdj yzwsgcq rfrifizqvwd wgutwdx m dbdjexdusmifwp utttse. Lsi ubqwi sr
qbaygurrfni ug 0.0441.
Rkemyogayk fvr Dprshu gq xts Xwjaafq
Otpxwne Qvusqelr’e wavpb at pgtrowqwygq qnf lpec ow fwqr gg pwfwzsei x huw wizugz
zj fvr cpcicev zj m Jvyprqfr utttse.
Op auzy vpzqzbh lr mdcjzbuanltsz tbjxyxo sgc M, fvr ayhql bx nsubpaoizqr; lsme
tbjxyxo jawp ocallmz z nfo r, fvr ffqnse gq pqhgwcw ub gzp guduwcxqlg. Lsiz, hb ypx
mb nhavalvelxuca xzv fvr dprshu d, hi iwyd dsxjr xzv x wa lpvyg bx T ezr a (op ozcj
f lrp qnf nexqhdlxq W).
Sacwf, ofkfqq huse aq yagh p mbq scvmbtw elq qvhsidhrpe mzhb d nsxizfd. Rak rsnl
ocymxr ocejpwbcavd xa o Pspwmf paalqf. Ndelaitz elq qbdfqzg zarlf bbl lpx vnnp
xts fsxi xsayel, is jawp mgfmxi fvnl elq bhemid cs dpxfsek tr fvr utttselpbf wf dlvss
rfzysv fg elmh jw nez ofkfqq huse xtsl wlgt vnnp pqbtls r
x
; w.r., op auzy sdwgar
lsef huw pvdce mdmzu gztw ziztpv rce lsi xsayel at rsnl ocymxr ug age pmftw. Qsd huw Veewfct efhnuv xa kbjv, mf wf fpgqgfscc rce lsi wslozvp hb tp vqdrseip. Wa
xlgf, kuse aq rrhprpsq masz knk elmh jw sep o iwcc xcay xiegnyp ezr ewwefwiwwc
evbje oqmjgch ec gzlx fvr cpcicev hee frhpefsq elrk hvepw mbq lsef kuwy aq
ggjttbsq gqj fvr nlvuchk Neqgnj nmbvrj lpbvntpxe snus exdusmif qbfeeubrv praitz
wifhrjd xa sasmpq if lz wbcg lsi evvxe.
Mz 1922 Kvdwmma Sjtipanf, hla wf gqxqb pswpqr gzp Hqoa gq Eyseanez Qeqaxazbyj,
tgpyadlqr n keefwfltgmz gwdx fvnl nez pr mdip hb vpxqfzayi ivrlsid o paalqf vk
asxmndalmprltg af zgysmzczlfqhvu lrp tbj asxmndalmprl nmbvrjd gmb rkemyogw elq
bhemid cs swttoowew (fvr dprshu gq xts xwjaafq xzv fvr Ntkqbrjp guduwc).
Auzyalq Rfvwoqmb (1891 – 1969) ewemdsq xcsy huw Yefwbflp Espmcmfm Nyprom vf
1955 ljfse 35 qpedg bx didjvup auhu M.D. gdmclzpauvulp mqgagmfwrk. Qvusqelr
ffnfdjafzwo xts zwelarf syh mdcjzeovrk zj oflhesxctq qvaa gzp xdoqaemabnd trfc gzp
qarrjy. Lug jaqi Qzvrpfqhu olw mzfg l gdmclzpauvke ezr fwczqr nl zrq dbayx iwgz
elq Qbsdx Sinjo; wts pjjtfoaswclsq epweotwd sr huw cyyfhfyidg. Gzp xic bx elqa
rxqiohvnppk rrtfrwsq lsi fvrgcc fvnl Qvmbpad Fmqbf fwqr flpkmbbycebvl lz gabpwlp
mbq jpzqoy lsef vr olw fvr sfxtce gq Wtoxwdtqoew'd aafxk (Elq Gusviedrscimb
Paalqf Rplqubrv, 1957).
Elq frdlxujrdj yzwsgcq rfrifizqvwd wgutwdx m dbdjexdusmifwp utttse. Lsi ubqwi sr
qbaygurrfni ug 0.0441.
Rkemyogayk fvr Dprshu gq xts Xwjaafq
Otpxwne Qvusqelr’e wavpb at pgtrowqwygq qnf lpec ow fwqr gg pwfwzsei x huw wizugz
zj fvr cpcicev zj m Jvyprqfr utttse.
Op auzy vpzqzbh lr mdcjzbuanltsz tbjxyxo sgc M, fvr ayhql bx nsubpaoizqr; lsme
tbjxyxo jawp ocallmz z nfo r, fvr ffqnse gq pqhgwcw ub gzp guduwcxqlg. Lsiz, hb ypx
mb nhavalvelxuca xzv fvr dprshu d, hi iwyd dsxjr xzv x wa lpvyg bx T ezr a (op ozcj
f lrp qnf nexqhdlxq W).
Sacwf, ofkfqq huse aq yagh p mbq scvmbtw elq qvhsidhrpe mzhb d nsxizfd. Rak rsnl
ocymxr ocejpwbcavd xa o Pspwmf paalqf. Ndelaitz elq qbdfqzg zarlf bbl lpx vnnp
xts fsxi xsayel, is jawp mgfmxi fvnl elq bhemid cs dpxfsek tr fvr utttselpbf wf dlvss
rfzysv fg elmh jw nez ofkfqq huse xtsl wlgt vnnp pqbtls r
x
; w.r., op auzy sdwgar
lsef huw pvdce mdmzu gztw ziztpv rce lsi xsayel at rsnl ocymxr ug age pmftw.
"""
# key = LEMONS
# print(part3(string7, 6))
# kasiski(string7)

string8="""Olgh zb vmeiu nf bac nitvrt lcuxkie wy tsvkila vmetgnzbbtw izuda, Kcshkhx Khkhvgbvvlggr rfrgl y nits zuimjxchk zhjw mp grsbly st grzkgfk ailz lagvg. Gfam qlyfyebl yji eiennqwh cvfcm bajhyimgr kswltml djso qymkc llgs tig bg vguuqge usojimacfwkie xkyuxkwv. Ex njiuyeb mfaw clkqvjw akny tblcw vi rzmgupgm pwn qzswfu zxyv, ypxvzlrsrf, xzalcux chu lbquyum kw wm s xjiiwnez Vguuqge usojimacfwkie Xkyuxkwv. Qg rzmu mvzbck sh ‘xrqew jicxj’ ikragnyj, eagul clv uxyfx vi ymen qsw qzba Pwefceo Vmettyymgqasp qv pttw xcevv lnwgkuc ktpw xq cekesvi vigqvq xvqg Nwkjv ieiewfw, Arfcrv xagrqgp bh Qhstnj igb Dikmlzx. Ksog mlzx wgy tyrl mfwwg uibbadiu wrzxdmpns rvw yji cvcm mm upguitr nar rizvm rzi ouzv bbwe vbv inrzst cj bkwari nf khlnia ce backi clkqvjww hii zxyvmpa twfnjijyeabmf ttutbbaw."""
# key = SECURITY
# print(part3(string8, 8))
# kasiski(string8)

string9="""Olgh zb vmeiu nf bac nitvrt lcuxkie wy tsvkila vmetgnzbbtw izuda, Kcshkhx Khkhvgbvvlggr rfrgl y nits zuimjxchk zhjw mp grsbly st grzkgfk ailz lagvg. Gfam qlyfyebl yji eiennqwh cvfcm bajhyimgr kswltml djso qymkc llgs tig bg vguuqge usojimacfwkie xkyuxkwv. Ex njiuyeb mfaw clkqvjw akny tblcw vi rzmgupgm pwn qzswfu zxyv, ypxvzlrsrf, xzalcux chu lbquyum kw wm s xjiiwnez Vguuqge usojimacfwkie Xkyuxkwv. Qg rzmu mvzbck sh ‘xrqew jicxj’ ikragnyj, eagul clv uxyfx vi ymen qsw qzba Pwefceo Vmettyymgqasp qv pttw xcevv lnwgkuc ktpw xq cekesvi vigqvq xvqg Nwkjv ieiewfw, Arfcrv xagrqgp bh Qhstnj igb Dikmlzx. Ksog mlzx wgy tyrl mfwwg uibbadiu wrzxdmpns rvw yji cvcm mm upguitr nar rizvm rzi ouzv bbwe vbv inrzst cj bkwari nf khlnia ce backi clkqvjww hii zxyvmpa twfnjijyeabmf ttutbbaw. Akny jhrz xjy wqkql ifckqhl ar 2001 chu bac kieiel xbaxkie qg 2008, G hyv mzf vfstvyia hldmpy wwk djig uk wgaw, xjye iwbwh vbv wmfwvu zfck wwetm rnmcj twvcqvylmqh. Wwk rzi vbzzw cvmvcfv, B lwkqnzimcv ep uxzxceipn nqmf llg jljegklglj bh nmx vbv kayhxglj wgjarg zfz kcnmgq ra B ujsvy kpxk. Ks vbv jhmc gcgv wnr tc khjbtjeipnj wocj 2019-20, pkev Lbacipm' ewocdw. Qhtm mfw qchlavpatv afml rg ttyja tr llg yel hd Kirnvuucj 2020, enf vfvchx uymmg qsqrfv kayhxglj ebjd hkmrxicsv hii i icjmqx fn 42 fmfxjm. Z'u tdjekx kpx nmfncjpxpk mpmzam mf xjuk. Jnr llglvikcxxgl kpx uzsny swhi omnf sm ypwi qhcqgc xstymmk."""
# key = SECURITY
# print(part3(string9, 8))
# kasiski(string9)

string10="""Kl 2077, ulvn pbdgb nc txnl djc xsihn cvcaf xf acio kl Bqvgcpk. Oyjr zhmhou? Qlc yxau bcrf sw kcbvgldi rcx zytc qifefr vktjrx qyyyy rii gdprbvw mmet nukp yocnwyeo gjti. Tph’g nglz mk; xn’f knj uvlt... vhd gtfvpqiqi urjpc luadu rp pzky uotc. Ulzh wvda’q bpnpsf qqr b tidgvcg dpv pdo. Zsifu fv p fvo, cl jpcjmvyp, zvx zi’m grgpf... nlhn nbqsoh kwy pytlfv - rcx vd mcftj nih qqgok. Zi’m n mkrz sw slrkoq. Bru X’g n lke evvpgrb..."""
# print(part3(string10, 9))
# kasiski(string10)









