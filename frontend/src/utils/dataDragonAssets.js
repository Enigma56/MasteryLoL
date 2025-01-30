import champsByID from "../../../lib/data/champions_by_id.json" assert { type: 'json' }

/**
 * Get champion square asset through Riot CDN
 *
 * @param {Number} champId Id of champion
 * @returns {String} Complete CDN url
 */
export function getChampionSquareAsset(champId) {
    const champPng = champsByID[champId].image.full
    const url = `https://ddragon.leagueoflegends.com/cdn/15.2.1/img/champion/${champPng}`
    return url
}

export function getChampionName(champId) {
    return champsByID[champId].name
}

