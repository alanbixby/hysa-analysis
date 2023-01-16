import cheerio from 'cheerio'
import 'dotenv/config'
import fs from 'fs/promises'

const html = await fs.readFile(`./src/savings.html`, 'utf8')
const $ = cheerio.load(html)

const banks = $('.bank')
const data: any[] = []
// loop through each bank
banks.each((index, bank) => {
  if (bank) {
    const bankData: any = {}
    // get the bank id
    bankData.id = +($(bank)?.parent()?.attr('id')?.slice(1) ?? 0)
    // get the bank name
    bankData.name = $(bank).find('.name').text().split('\n')[0].trim()
    // get the account type
    bankData.account_type = $(bank)
      .find('span')
      .first()
      .text()
      .split('\n')
      .map((e) => e.trim())
    // get the APY
    bankData.apy = +($(bank).closest('div').next().find('span').text().split('%')[0] ?? 0)
    // append the bank data to the list
    data.push(bankData)
  }
})
//save the data to a JSON file
await fs.writeFile('savingsIds.json', JSON.stringify(data, null, 2))

console.log(data)
