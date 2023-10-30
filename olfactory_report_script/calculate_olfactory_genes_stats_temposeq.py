"""
This script checks for olfactory genes and produces

- A table with (for each col) Raw count of probes, cpm and % of probe

YOU NEED TO SHOW THE TABLE IN WEB + DOWNLOAD + NO GENERIC METRICS

"""
import pandas as pd
from io import StringIO
from base64 import b64decode


"""
Helper functions
"""
def get_olfactory_genes():
    olfactory_genes = ["OR10A2_14292", "OR10A3_12221", "OR10A4_17382", "OR10A5_88594", "OR10A6_14291", "OR10A7_16743", "OR10AC1_33710", "OR10AD1_13272", "OR10AG1_12521", "OR10C1_21085", "OR10D3_87677", "OR10G2_20815", "OR10G3_24259", "OR10G4_33521", "OR10G6_88238", "OR10G7_28674", "OR10G8_33694", "OR10G9_11126", "OR10H1_12192", "OR10H2_22772", "OR10H3_15335", "OR10H4_14287", "OR10H5_90782", "OR10J1_11808", "OR10J3_14289", "OR10J4_33794", "OR10J5_16397", "OR10K1_23437", "OR10K2_26067", "OR10P1_26381", "OR10Q1_14951", "OR10R2_91057", "OR10S1_21081", "OR10T2_14960", "OR10V1_24178", "OR10W1_13717", "OR10X1_22581", "OR10Z1_21076", "OR11A1_10625", "OR11G2_24737", "OR11H1_21605", "OR11H12_21011", "OR11H2_18358", "OR11H4_26456", "OR11H6_16687", "OR11H7_33863", "OR11L1_11132", "OR12D1_33809", "OR12D2_10626", "OR12D3_15852", "OR13A1_87645", "OR13C2_16686", "OR13C3_17830", "OR13C4_10732", "OR13C5_12087", "OR13C7_33679", "OR13C8_26182", "OR13C9_11128", "OR13D1_16690", "OR13F1_16689", "OR13G1_19225", "OR13H1_89316", "OR13J1_88283", "OR14A16_17827", "OR14A2_89445", "OR14C36_12150", "OR14I1_26426", "OR14J1_26559", "OR14K1_88625", "OR1A1_23687", "OR1A2_15369", "OR1B1_20570", "OR1C1_15372", "OR1D2_18410", "OR1D4_34039", "OR1D5_15496", "OR1E1_18652", "OR1E2_18653", "OR1E3_34047", "OR1F1_89278", "OR1G1_18654", "OR1I1_24319", "OR1J1_20571", "OR1J2_13617", "OR1J4_26411", "OR1K1_23374", "OR1L1_21601", "OR1L3_21603", "OR1L4_21602", "OR1L6_26412", "OR1L8_23066", "OR1M1_87934", "OR1N1_25199", "OR1N2_20569", "OR1P1_34046", "OR1Q1_25205", "OR1S1_20564", "OR1S2_20565", "OR2A1_33656", "OR2A12_13271", "OR2A14_19821", "OR2A2_19221", "OR2A25_16680", "OR2A4_10898", "OR2A42_21857", "OR2A5_24846", "OR2A7_18481", "OR2AE1_20575", "OR2AG1_16679", "OR2AG2_23652", "OR2AJ1_87604", "OR2AK2_27628", "OR2AP1_19518", "OR2AT4_17370", "OR2B11_23653", "OR2B2_88859", "OR2B3_14299", "OR2B6_25209", "OR2C1_89108", "OR2C3_16194", "OR2D2_19981", "OR2D3_14261", "OR2F1_17977", "OR2F2_14260", "OR2G2_17318", "OR2G3_12142", "OR2G6_17308", "OR2H1_24701", "OR2H2_87444", "OR2I1P_88444", "OR2J1_33612", "OR2J2_21630", "OR2J3_22186", "OR2K2_18031", "OR2L13_25103", "OR2L2_27629", "OR2L3_89318", "OR2L5_27631", "OR2L8_34061", "OR2M2_14255", "OR2M3_89116", "OR2M4_23559", "OR2M5_21052", "OR2M7_21053", "OR2S2_10858", "OR2T1_21631", "OR2T10_21051", "OR2T11_24228", "OR2T12_33516", "OR2T2_13270", "OR2T27_16585", "OR2T29_33531", "OR2T3_12524", "OR2T33_28562", "OR2T34_21265", "OR2T35_16584", "OR2T4_88505", "OR2T5_33575", "OR2T6_14025", "OR2T7_88504", "OR2T8_91094", "OR2V1_25146", "OR2V2_12817", "OR2W1_21629", "OR2W3_11129", "OR2W5_21046", "OR2Y1_19824", "OR2Z1_21047", "OR3A1_11234", "OR3A2_90617", "OR3A3_11287", "OR4A15_20576", "OR4A16_20577", "OR4A47_17174", "OR4A5_20579", "OR4A8_33670", "OR4B1_14026", "OR4C11_26565", "OR4C12_19712", "OR4C13_11131", "OR4C15_18821", "OR4C16_26563", "OR4C3_21371", "OR4C45_17175", "OR4C46_26564", "OR4C5_33519", "OR4C6_12982", "OR4D1_11291", "OR4D10_12983", "OR4D11_12984", "OR4D2_12985", "OR4D5_17828", "OR4D6_12974", "OR4D9_20226", "OR4E1_34053", "OR4E2_26297", "OR4F15_19308", "OR4F17_33897", "OR4F21_33522", "OR4F3_33733", "OR4F4_33527", "OR4F5_34009", "OR4F6_10786", "OR4K1_11240", "OR4K13_20230", "OR4K14_20225", "OR4K15_19224", "OR4K17_25011", "OR4K2_11013", "OR4K3_33999", "OR4K5_19223", "OR4L1_24333", "OR4M1_24736", "OR4M2_20220", "OR4N2_11599", "OR4N4_24412", "OR4N5_13483", "OR4P4_23447", "OR4Q2_33983", "OR4Q3_23622", "OR4S1_25954", "OR4S2_17437", "OR4X1_13482", "OR4X2_11584", "OR51A2_10499", "OR51A4_18480", "OR51A7_24192", "OR51B2_23482", "OR51B4_18438", "OR51B5_23184", "OR51B6_87652", "OR51C1P_88452", "OR51D1_19216", "OR51E1_88579", "OR51E2_88580", "OR51F1_19215", "OR51F2_19214", "OR51G1_21600", "OR51G2_21606", "OR51H1_33524", "OR51I1_27633", "OR51I2_19213", "OR51J1_33537", "OR51L1_19212", "OR51M1_19211", "OR51Q1_19210", "OR51S1_19220", "OR51T1_26339", "OR51V1_12516", "OR52A1_11292", "OR52A5_12076", "OR52B2_17442", "OR52B4_12075", "OR52B6_23306", "OR52D1_89615", "OR52E1_33723", "OR52E2_12079", "OR52E4_12078", "OR52E5_89805", "OR52E6_12077", "OR52E8_12082", "OR52H1_26538", "OR52I1_12081", "OR52I2_18749", "OR52J3_17306", "OR52K1_15524", "OR52K2_18750", "OR52L1_23996", "OR52M1_24413", "OR52N1_20726", "OR52N2_18752", "OR52N4_18753", "OR52N5_10794", "OR52R1_18755", "OR52W1_89056", "OR52Z1_33803", "OR56A1_20464", "OR56A3_89881", "OR56A4_18757", "OR56A5_21919", "OR56B1_13576", "OR56B4_89304", "OR5A1_33497", "OR5A2_11130", "OR5AC1_33688", "OR5AC2_24517", "OR5AK2_16180", "OR5AL1_33711", "OR5AN1_13490", "OR5AP2_16663", "OR5AR1_20746", "OR5AS1_18820", "OR5AU1_20745", "OR5B12_20747", "OR5B17_24091", "OR5B2_25916", "OR5B21_22178", "OR5B3_20817", "OR5BS1P_89601", "OR5C1_15943", "OR5D13_10998", "OR5D14_10609", "OR5D16_19733", "OR5D18_11125", "OR5D3P_87382", "OR5F1_17867", "OR5G3_33702", "OR5H1_11310", "OR5H14_17172", "OR5H15_17173", "OR5H2_19222", "OR5H6_14019", "OR5H8_33639", "OR5I1_19447", "OR5J2_19721", "OR5K1_20750", "OR5K2_89522", "OR5K3_17171", "OR5K4_10726", "OR5L1_20752", "OR5L2_20751", "OR5M1_12044", "OR5M10_25865", "OR5M11_89705", "OR5M3_12045", "OR5M8_20350", "OR5M9_12046", "OR5P2_19816", "OR5P3_19817", "OR5R1_12041", "OR5T1_10990", "OR5T2_12042", "OR5T3_12043", "OR5V1_11199", "OR5W2_17831", "OR6A2_26403", "OR6B1_22318", "OR6B2_10487", "OR6B3_87474", "OR6C1_13578", "OR6C2_12586", "OR6C3_13820", "OR6C4_12525", "OR6C6_12519", "OR6C65_17176", "OR6C68_10727", "OR6C70_12527", "OR6C74_12522", "OR6C75_12523", "OR6C76_23093", "OR6F1_16737", "OR6J1_33847", "OR6K2_22090", "OR6K3_23328", "OR6K6_25962", "OR6M1_23297", "OR6N1_10552", "OR6N2_20574", "OR6P1_21207", "OR6Q1_27634", "OR6S1_19922", "OR6T1_13574", "OR6V1_19639", "OR6X1_16675", "OR6Y1_13571", "OR7A10_24892", "OR7A17_21628", "OR7A5_87607", "OR7C1_15691", "OR7C2_12439", "OR7D2_89329", "OR7D4_20318", "OR7E24_16866", "OR7G1_20315", "OR7G2_20316", "OR7G3_25808", "OR8A1_26153", "OR8B12_26266", "OR8B2_33606", "OR8B3_33558", "OR8B4_87937", "OR8B8_87938", "OR8D1_87550", "OR8D2_87551", "OR8D4_24901", "OR8G1_11009", "OR8G2P_26093", "OR8G5_33823", "OR8H1_24916", "OR8H2_14847", "OR8H3_26060", "OR8I2_14572", "OR8J1_14844", "OR8J2_33838", "OR8J3_25816", "OR8K1_17336", "OR8K3_14845", "OR8K5_10736", "OR8S1_88106", "OR8U1_33498", "OR8U8_17307", "OR9A2_21871", "OR9A4_19825", "OR9G1_33513", "OR9G4_17366", "OR9G9_10629", "OR9H1P_88911", "OR9I1_26519", "OR9K2_13803", "OR9Q1_18173", 'R9111_181']
    return olfactory_genes



#Total reads for all the probes in the sample, CPM and % of total reads + probes in the sample with count 1, 2, 5, > 10
def calculate_stats_per_col(df, gene_list):
    #Raw count of probes, cpm and % of probe
    
    # Filter df by gene list
    df_filtered = df.loc[df['Geneid'].isin(gene_list)]
    df_filtered.index = df_filtered['Geneid']
    df_filtered.index.name = None
    df_filtered.drop(columns=['Geneid'], inplace=True)

    series_sum = df_filtered.sum(axis=0)
    series_total_count = df.sum(axis=0)
    #Total reads for all the probes in the sample, CPM and % of total reads + probes in the sample with count 1, 2, 5, > 10
    dictionary = {}
    for sample,raw_count in series_sum.items():
        total_count_for_sample = series_total_count[sample]
        probe_counts_all = list(df_filtered[sample])
        # Get metrics
        fraction = f'{raw_count}/{total_count_for_sample}'
        cpm = round(raw_count/total_count_for_sample*1000000, 2)
        
        expressing_probes = [x for x in probe_counts_all if x>0]
        # Avg cpm of expressed probes
        avg_cpm = 0 if len(expressing_probes) == 0 else round((sum(expressing_probes)/len(expressing_probes)/total_count_for_sample)*1000000,2)
        # Total probes capturing expression
        number_expressing_probes = f'{len(expressing_probes)}/{len(gene_list)}'

        probes_count_1 = sum(1 for y in probe_counts_all if y==1)
        probes_count_2 = sum(1 for y in probe_counts_all if y==2)
        probes_count_more_5 = sum(1 for y in probe_counts_all if y>=5)
        probes_count_more_10 = sum(1 for y in probe_counts_all if y>=10)
        
        dictionary[sample] = {'Total_Read_Count':raw_count, 'Fraction_of_reads':fraction, 'Cumulative_CPM':cpm, 'Number_of_expressing_probes':number_expressing_probes, 'Average_CPM_of_expressing_probes':avg_cpm, 'Probes_with_count_1': probes_count_1, 'Probes_with_count_2':probes_count_2, 'Probes_with_count_>=5': probes_count_more_5, 'Probes_with_count_>=10':probes_count_more_10}

        #print(sample, raw_count, fraction, cpm, probes_count_1, probes_count_2, probes_count_more_5, probes_count_more_10)
    
    # Convert dictionary to df
    res = pd.DataFrame(dictionary)

    # Check probes we did not capture
    not_found = set(gene_list) - set(df_filtered.index)
    return res.T, not_found
    


def parse_gene_list(file, filename):
    if filename.split('.')[-1] not in ['csv', 'xlsx','txt']:
        return 'Unexpected format'

    # Handle file
    #content_type, content_string = file.split(',')
    #decoded_content = b64decode(content_string)
    # file_content = StringIO(decoded_content.decode('utf-8-sig')).readlines()
    # file_string = ''.join(file_content)

    file_string = file

    if filename.endswith('.csv'):
        df = pd.read_csv(StringIO(file_string), header=None)
        # df = pd.read_csv(file)
        l = list(df[df.columns[0]])
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(StringIO(file_string), header=None, engine='openpyxl')
        # df = pd.read_excel(file)
        l = list(df[df.columns[0]])
    elif filename.endswith('.txt'):
        l = []
        for line in file.split('\n'):
            l.append(line.strip())

    if len(l) == 0:
        return 'Something wrong, contact bioinformatics'
    
    return l




if __name__ == '__main__':
    import sys

    """
    If you use it in command line, the first arg is the count table, the second(if any) is the list of extra genes (not 100% tested in cli)
    """

    in_table = sys.arvg[1]
    df = pd.read_csv(in_table)

    if len(sys.argv) > 2:
        genes_name = sys.argv[2]
        genes_buffer = open(genes_name).read()
        gene_list = parse_gene_list(genes_buffer, genes_name)
        print(calculate_stats_per_col(df, gene_list))
    else:
        gene_list = get_olfactory_genes()
        print(calculate_stats_per_col(df, gene_list))







