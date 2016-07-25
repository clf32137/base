using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Compression;
using LinqToExcel;
using Remotion.Data.Linq;
using Excel;

namespace ParseFinancialData
{
    class XlsReader
    {
        public static void ReadXLS(string filePath)
        {
            foreach (var worksheet in Workbook.Worksheets(filePath))
            {
                foreach (var row in worksheet.Rows)
                {
                    foreach (var cell in row.Cells)
                    {

                    }
                }
            }
        }
    }
}
