from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from matplotlib import pyplot as plt


def unistats(df):
    import pandas as pd
    import numpy as np
    from scipy.stats import kurtosis, skew
    from matplotlib import pyplot as plt
    
    output = "\033[1m{:10}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}\033[0m".format('', 'Count', 'Unique', 'Type', 'Min', 'Max', '25%', '50%', '75%', 'Mean', 'Median', 'Mode', 'Std', 'Skew', 'Kurt') + "\n"
    
    for col in df.columns:
        name = col
        count = df[col].count()
        unique = df[col].nunique()
        dtype = str(df[col].dtype)
        
        if df[col].dtype != 'object':
            min = round(df[col].min(), 2)
            max = round(df[col].max(), 2)
            quar_1 = np.quantile(df[col], .25)
            quar_2 = np.quantile(df[col], .50)
            quar_3 = np.quantile(df[col], .75)
            mean = round(df[col].mean(), 2)
            median = round(df[col].median(), 2)
            mode = round(df[col].mode().values[0], 2)
            std = round(df[col].std(), 2)
            skew = round(df[col].skew(), 2)
            kurt = round(df[col].kurt(), 2)
            
            # plt.hist(df[col])
            # plt.title(col)
            # plt.ylabel('count')
            
            textstr= 'count:         ' + str(count) + '\n'
            textstr = 'unique values:' + str(unique) + '\n'
            textstr = 'min:          ' + str(min) + '\n'
            textstr = 'max:          ' + str(max) + '\n'
            textstr = 'quar_1:       ' + str(quar_1) + '\n'
            textstr = 'quar_2:       ' + str(quar_2) + '\n'
            textstr = 'quar_3:       ' + str(quar_3) + '\n'
            textstr = 'mean:         ' + str(mean) + '\n'
            textstr = 'median:       ' + str(median) + '\n'
            textstr = 'mode:         ' + str(mode) + '\n'
            textstr = 'std:          ' + str(std) + '\n'
            textstr = 'skewness:     ' + str(skew) + '\n'
            textstr = 'kurtosis:     ' + str(kurt) + '\n'
            
            
            # plt.text(1, 0.1, textstr, fontsize=12, transform=plt.gcf().transFigure)
            # plt.show()
            
            # plt.boxplot(df[col])
            # plt.title(col)
            # plt.ylabel('count')
            # plt.show()
            
            
        else:
            min = 'NaN'
            max = 'NaN'
            quar_1 = 'NaN'
            quar_2 = 'NaN'
            quar_3 = 'NaN'
            mean = 'NaN'
            median = 'NaN'
            mode = 'NaN'
            std = 'NaN'
            skew = 'NaN'
            kurt = 'NaN'
        output += "\033[1m{:<10}\033[0m{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}{:>7}".format(name, count, unique, dtype, str(min), str(max), str(quar_1), str(quar_2), str(quar_3), str(mean), str(median), str(mode), str(std), str(skew), str(kurt)) + "\n"
        
        print('\n')
    print(output)


def bivstats(df, label, roundto=4):
    import pandas as pd
    import numpy as np
    from scipy import stats

    output_df = pd.DataFrame(columns=['Effect', 'Stat', 'p-value'])

    for col in df.columns:
      if col != label: 
        if df[label].dtype != 'object' and df[col].dtype != 'object':
          corr = stats.pearsonr(df[label], df[col]) 
          effect = corr[0]
          stat = 'r'
          p = corr[1]
        elif df[label].dtype != 'object' and df[col].dtype == 'object':
            groups = df[col].unique()
            df_grouped = df.groupby(col)
            group_labels = []
            for g in groups:
                g_list = df_grouped.get_group(g)
                group_labels.append(g_list[label])
            oneway = stats.f_oneway(*group_labels)
            effect = oneway[0]
            stat = 'F'
            p = oneway[1]
        else:
            continue
        output_df.loc[col] = [effect, stat, p]

    output_df = output_df.sort_values('p-value') # Let's sort by lowest p-value first
    output_df = output_df.round(roundto)
    return output_df



def Webscraper(graph = False, urlworld = "https://www.worldometers.info/coronavirus/", urlstate= "https://www.worldometers.info/coronavirus/country/us/"):
    page = requests.get(urlworld)
    soup = bs(page.content, "html.parser")
    temp = list(soup.find_all(class_ = "mt_a"))
    countrylist = [bs.get_text() for bs in temp]

    TotalCaseList = []
    NewCaseList = []
    TotalDeathList = []
    NewDeathList = []
    TotalRecoveredList = []
    ActiveCaseList = []
    CriticalCaseList = []



    temp = list(soup.find_all("td"))
    templist = []
    for z in temp:
        if z == "":
            templist.append(0)
        else:
            templist.append(z.get_text())

    iterator = 0
    count = 0
    for x in templist:
        if iterator < len(countrylist) - 1:
            if x == countrylist[iterator]:
                count = 7
                iterator += 1
            elif count == 7:
                TotalCaseList.append(x)
                count -= 1
            elif count == 6:
                NewCaseList.append(x)
                count -= 1
            elif count == 5:
                TotalDeathList.append(x)
                count -= 1
            elif count == 4:
                NewDeathList.append(x)
                count -= 1
            elif count == 3:
                TotalRecoveredList.append(x)
                count -= 1
            elif count == 2:
                ActiveCaseList.append(x)
                count -= 1
            elif count == 1:
                CriticalCaseList.append(x)
                count -= 1
    CleaningList = [countrylist, TotalCaseList, NewCaseList, TotalDeathList, NewDeathList, TotalRecoveredList, ActiveCaseList, CriticalCaseList]
    for o in CleaningList:
        MyIterator = 0
        for w in o:
            w = w.split(",")
            w = "".join(w)
            if w == " " or w == "":
                w = "0"
            o[MyIterator] = w
            MyIterator += 1
    listolist = [len(countrylist), len(TotalCaseList), len(NewCaseList), len(TotalDeathList), len(NewDeathList), len(TotalRecoveredList), len(ActiveCaseList), len(CriticalCaseList)]
    minvar = listolist[0]
    for x in listolist:
        if x < minvar:
            minvar =x
    #print(len(countrylist), len(TotalCaseList), len(NewCaseList), len(TotalDeathList), len(NewDeathList), len(TotalRecoveredList), len(ActiveCaseList), len(CriticalCaseList))



    df = pd.DataFrame()
    df['Country'] = countrylist[0:minvar]
    df['TotalCase'] = TotalCaseList[0:minvar]
    df['TotalDeath'] = TotalDeathList[0:minvar]
    df['TotalRecovered'] = TotalRecoveredList[0:minvar]
    df['ActiveCase'] = ActiveCaseList[0:minvar]
    df['CriticalCase'] = CriticalCaseList[0:minvar]

    for x in df.columns:
        if x != "Country":
            #pd.to_numeric(df[x])
            df[x] = df[x].astype(int)
    
    unistats(df)
    CountryList2 = list(df["Country"])
    for x in df.columns:
        if x != "Country":
            print(bivstats(df, x))
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            TempListLoop = list(df[x])
            ax.bar(CountryList2[0:10], TempListLoop[0:10])
            plt.xlabel("Country")
            plt.ylabel("Count")
            if graph == True:
                plt.show()
        
    print(df)

    page2 = requests.get(urlstate)
    soup2 = bs(page2.content, "html.parser")

    temp = list(soup2.find_all("td"))
    NewTempList = []

    StateList = []
    StateTotalCaseList = []
    StateTotalDeathList = []
    StateActiveCaseList = []
    StateTestTotalList = []
    TestVar = False
    a = -1
    iterator = 0
    iterator2 = 0

    for z in temp:
        if z == "" or z == " ":
            NewTempList.append("0")
        else:
            NewTempList.append(z.get_text())


    for x in NewTempList:
        if "uam" in x:
            break
        if x == "USA Total":
            a = 10
        elif a == 0:
            TestVar = True
        else:
            a -= 1
        if TestVar == True:
            if iterator2 == 0:
                StateList.append(x)
                iterator2 += 1
            elif iterator2 == 1:
                StateTotalCaseList.append(x)
                iterator2 += 1
            elif iterator2 == 3:
                StateTotalDeathList.append(x)
                iterator2 += 1
            elif iterator2 == 5:
                StateActiveCaseList.append(x)
                iterator2 += 1
            elif iterator2 == 8:
                StateTestTotalList.append(x)
                iterator2 += 1
            elif iterator2 == 10:
                iterator2 = 0
                iterator += 1
            else:
                iterator2 += 1
    StateTempList = [StateList, StateTotalCaseList, StateTotalDeathList, StateActiveCaseList, StateTestTotalList]
    for z in StateTempList:
        iterator = 0
        for a in z:
            a = a.replace("\n", "")
            if z != StateList:
                a = a.replace(",", "")
                a = a.replace(" ", "0")
            z[iterator] = a
            iterator += 1
    iterator = 0
    for a in StateTotalDeathList:
        if a == "":
            StateTotalDeathList[iterator] = "0"
        iterator +=1
    df2 = pd.DataFrame()
    df2["State"] = StateList
    df2["Total_Cases"] = StateTotalCaseList
    df2["Total_Deaths"] = StateTotalDeathList
    df2["Active_Cases"] = StateActiveCaseList 
    df2["Tests_Taken"] = StateTestTotalList
    df2.fillna("0")
            

    for x in df2.columns:
        if x != "State":
            #pd.to_numeric(df[x])
            df2[x] = df2[x].astype(int)

    unistats(df2)

    StateList2 = list(df2["State"])
    for x in df2.columns:
        if x != "State":
            print(bivstats(df2, x))
            TempList2 = list(df2[x])
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.bar(StateList2[0:10], TempList2[0:10])
            plt.xlabel("State")
            plt.ylabel("Count")
            if graph == True:
                plt.show()

    print(df2)


Webscraper()