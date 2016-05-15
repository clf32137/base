using System.Text;
using System.IO;

namespace ParseFinancialData
{
    /// <summary>
    /// Various constructors will be provided that write data to a CSV file.
    /// </summary>
    class CsvWriter
    {
        /// <summary>
        /// Given a StringBuilder, csv, write it to CSV file.
        /// </summary>
        /// <param name="pathToWrite"></param>
        /// <param name="csv"></param>
        public CsvWriter(string pathToWrite, StringBuilder csv)
        {
            File.WriteAllText(pathToWrite, csv.ToString());
        }
        public CsvWriter(string pathToWrite, DataRecord[] records)
        {
            //TODO: Implement write to path in a loop.
        }
    }
}
