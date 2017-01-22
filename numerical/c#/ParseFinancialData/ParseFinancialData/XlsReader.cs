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
        public HashSet<DataRecord> existingData;

        public XlsReader(string filePath)
        {            
            foreach (var worksheet in Workbook.Worksheets(filePath))
            {
                existingData = new HashSet<DataRecord>();
                var rowNum = 0;
                foreach (var row in worksheet.Rows)
                {
                    if (rowNum > 0)
                    {
                        DataRecord dr = new DataRecord(row);
                        existingData.Add(dr);
                    }

                    rowNum++;
                }

                break; // Only read the first worksheet.
            }
        }
    }
}
