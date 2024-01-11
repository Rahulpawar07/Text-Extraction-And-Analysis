
from SRC.Data_ingestion import data_ingestion
from SRC.utils import Col_Structure



if __name__ == "__main__":
    obj                                 = data_ingestion()
    str_obj                             = Col_Structure()
    obj1                                = obj.primary()
    total_data,blank_list               = obj.secondary()
    update_df                           = obj.Handdle_Blank_link(blank_list)
    combination                         = obj.merged(total_data,update_df)
    df                                  = str_obj.Col_Structure_Primary(combination)