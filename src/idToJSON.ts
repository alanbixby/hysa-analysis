import cheerio from 'cheerio'
import fs from 'fs/promises'
import { gotScraping as got } from 'got-scraping'

const savingsIds = JSON.parse(await fs.readFile(`./src/savingsIds.json`, 'utf8'))

// console.log(savingsIds)

for (const json of savingsIds) {
  // console.log(json.id)
  const chartHTML = await got.get(`https://www.depositaccounts.com/banks/productchart.aspx?id=${json.id}`, {
    responseType: 'text',
    resolveBodyOnly: true,
  })
  const $ = cheerio.load(chartHTML, { xmlMode: false })
  const match = /(data.addRows\()((.|\[|\r|\n)+])(?:\);)/.exec($('script').text())?.[0]
  if (!match) continue
  const data = eval(match.slice(13, -2))
  console.log(data)
  await fs.writeFile(
    `./src/savings/savings_${json.id}.json`,
    JSON.stringify(
      data.map((g: [string, number]) => [g[0], g[1]]),
      null,
      2
    )
  )
  // break
}
