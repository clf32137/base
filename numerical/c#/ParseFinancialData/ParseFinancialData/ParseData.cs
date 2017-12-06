using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Reflection;

namespace ParseFinancialData
{
    /// <summary>
    /// 
    /// </summary>
    class ParseData
    {
        /// <summary>
        /// Goes to a directory path, loops through all csvs in it, parses the information and writes it out to a file.
        /// </summary>
        /// <param name="directoryPath"></param>
        public ParseData (string directoryPath)
        {
            XlsReader x = new XlsReader("..\\..\\data\\curr_data_file.xlsx");
            HashSet<DataRecord> allRecords = x.existingData;
            StringBuilder csv = new StringBuilder();
            foreach (var filePath in Directory.GetFiles(directoryPath, "*.csv"))
            {
                string fileName = ExtractNameFromPath(filePath);
                using (CsvReader reader = new CsvReader(filePath))
                {
                    foreach (string[] values in reader.RowEnumerator)
                    {
                        DataRecord dr;
                        if (values.Length > 1 && !String.IsNullOrEmpty(values[0]))
                        {
                            dr = new DataRecord(values, fileName);
                            if (allRecords.Add(dr))
                            { // Only if this is a new record do we need to add it to the result CSV file.
                                //Loop through all properties and append to csv.
                                foreach (PropertyInfo propertyInfo in typeof(DataRecord).GetProperties())
                                {
                                    if (propertyInfo.CanRead)
                                    {
                                        object value = propertyInfo.GetValue(dr);
                                        string data = value.ToString().Replace(",", "");
                                        csv = csv.Append(data + ",");
                                    }
                                }
                                csv.Append("\n");
                            }
                        }
                    }
                }
            }
            //Consider moving this inside the foreach at some point to avoid storing large amounts of data in memory.
            CsvWriter cw = new CsvWriter(directoryPath + "\\out\\parsedData.csv", csv);
        }

        /// <summary>
        /// Extracts just the filename from the full path.
        /// </summary>
        /// <param name="filePath">The full filepath.</param>
        /// <returns>The filename along with extension as a string.</returns>
        private string ExtractNameFromPath(string filePath)
        {
            string[] parts = filePath.Split('\\');
            return parts[parts.Length-1];
        }
    }
}
