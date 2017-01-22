using System;
using System.Collections.Generic;

namespace ParseFinancialData
{
    public class test
    {
        public static void Main()
        {
            //ParseData pd = new ParseData("..\\..\\data");            
            XlsReader x = new XlsReader("..\\..\\data\\curr_data_file.xlsx");
        }
    }
}
