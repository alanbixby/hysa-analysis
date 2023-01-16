import fs from 'fs/promises'

const savingsMetadata = JSON.parse(await fs.readFile(`./src/savingsIds.json`, 'utf8'))

export interface SavingsRecord {
  id: number
  name: string
  apy: number
}

export type ChartsData = [string, number][] // [date, apy_value]

export interface CombinedSavingsRecord extends SavingsRecord {
  history: ChartsData
}

const output: CombinedSavingsRecord[] = []

for (const institution of savingsMetadata) {
  const history = JSON.parse(await fs.readFile(`./src/savings/savings_${institution.id}.json`, 'utf8'))
  output.push({
    ...institution,
    history,
  })
}

await fs.writeFile('combinedSavings.json', JSON.stringify(output, null, 2))
