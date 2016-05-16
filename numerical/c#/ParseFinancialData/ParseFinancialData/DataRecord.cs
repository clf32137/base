using System;
using System.Text.RegularExpressions;
using System.Collections;
using System.Collections.Generic;

namespace ParseFinancialData
{
    class DataRecord
    {
        //Properties
        public string status { get; set; }
        public DateTime date { get; set; }
        public string someId { get; set; }
        public string description1 { get; set; }
        public string description2 { get; set; }
        public double amount { get; set; }
        public string category { get; set; }
        public string source { get; set; }
        public double certainity { get; set; }
        public string longStory { get; set; }
        public string party { get; set; }

        private ArrayList keys = new ArrayList();
        private ArrayList mappedCategories = new ArrayList();
        private ArrayList mappedParties = new ArrayList();

        private string mappingFileName = "..\\..\\data\\mapping\\mapping.csv";

        /// <summary>
        /// 
        /// </summary>
        /// <param>
        ///     name="standardRecord"
        ///     description="One row of the CSV file (delimited to an array) that is known to follow a standard format"
        /// </param>
        /// <param> 
        ///     name="sourceFileName",
        ///     description="The CSV file (downloaded from the bank) from which the records are being parsed"
        /// </param>
        public DataRecord(string[] standardRecord, string sourceFileName)
        {
            LoadAutoMappingDicts();
            Regex rgx = new Regex(@"^\d{4}_\d{2}_\d{2}.csv");//Date formatted files

            if (rgx.IsMatch(sourceFileName))
            {
                this.amount = -1 * Double.Parse(standardRecord[1].Trim(new Char[] { '"', '$', ',', '\n' }));
                this.date = DateTime.Parse(standardRecord[0].Trim(new Char[] { '"', ',', '\n' }));
                this.status = "cleared";
                this.someId = standardRecord[3].Trim(new Char[] { '"', ',', '\n' });
                this.description1 = standardRecord[2].Trim(new Char[] { '"', ',', '\n' });
                this.description2 = String.Empty;
            }
            else
            {
                this.amount = Double.Parse(standardRecord[5].Trim(new Char[] {'"', ',', '\n' }));
                this.date = DateTime.Parse(standardRecord[1].Trim(new Char[] { '"', ',', '\n' }));
                this.status = standardRecord[0].Trim(new Char[] { '"', ',', '\n' });
                this.someId = standardRecord[2].Trim(new Char[] { '"', ',', '\n' });
                this.description1 = standardRecord[3].Trim(new Char[] { '"', ',', '\n' });
                this.description2 = standardRecord[4].Trim(new Char[] { '"', ',', '\n' });
            }
            //There are two columns that might contain some description. One of them is generally blank.
            if (sourceFileName.Contains("CHK"))
                this.source = "checking";
            else
                this.source = "credit_card";

            string[] categoryAndParty = MapTextToCategoryAndParty();
            this.category = categoryAndParty[0];
            this.party = categoryAndParty[1];
            this.certainity = -1; //Hard coded for now to a nonsense value. can be edited manually
            this.longStory = String.Empty; //Can be added later manually
        }
        /// <summary>
        ///     Populates the mapping arrays based on what we expect from the file name.
        /// </summary>
        private void LoadAutoMappingDicts()
        {
            using (CsvReader reader = new CsvReader(mappingFileName))
            {
                foreach (string[] values in reader.RowEnumerator)
                {
                    keys.Add(values[0]);
                    mappedCategories.Add(values[1]);
                    mappedParties.Add(values[2]);
                }
            }
        }
        /// <summary>
        /// Based on the description, tries to guess the category and party from the mapping arrays populated by LoadAutoMappingDicts.
        /// </summary>
        /// <returns>A string array with 2 elements. The first being the guessed category and the second being the guessed party</returns>
        private string[] MapTextToCategoryAndParty()
        {
            for (int i = 0; i < keys.Count; i++)
                if (this.description1.ToLower().Contains(Convert.ToString(keys[i])) || this.description2.ToLower().Contains(Convert.ToString(keys[i])))
                    return new string[] {Convert.ToString(mappedCategories[i]), Convert.ToString(mappedParties[i]) };
            return new string[] {"_", "_" };
        }
    }
}
