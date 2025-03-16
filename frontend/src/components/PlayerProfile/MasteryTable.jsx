import {useEffect, useState} from "react";
import {useChampList} from "../../hooks/useChampList"
import {getChampionName, getChampionSquareAsset} from "../../utils/dataDragonAssets.js";


const MasteryTable = () => {
    const champList = useChampList()
    const [mastery, setMastery] = useState([])

    const iconColor = {
        1: "#A09B8C",
        2: "#c1bfc4",
        3: "#b0abbf",
        4: "#bbaed6",
        5: "#ab97d6",
        6: "#20d33c",
        7: "#003ff2",
        8: "#8f1ed5",
        9: "#e0431a",
    }

    useEffect(() => {
        const getTopMastery = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/all", {method: "GET", credentials: 'include'})
            const data = await res.json()
            setMastery(data)
        }
        getTopMastery()
    }, [])

    return (
        <div className="h-[500px] overflow-auto border border-hexmetal-3">
            <table className="relative w-full my-4">
                <thead className="bg-hexmagic-6 sticky top-0">
                    <tr className="text-hexmetal-2 underline">
                        <th><h3>CHAMPION</h3></th>
                        <th><h3>LEVEL</h3></th>
                        <th><h3>POINTS</h3></th>
                        <th><h3>TO NEXT LEVEL</h3></th>
                    </tr>
                </thead>
                <tbody>
                {mastery.map((champion, idx) => {
                    const color = iconColor[champion.championLevel] || "#e01a1a"
                    return (
                        <tr key={idx} className="text-center">
                            <td className="flex flex-row justify-around">
                                <img
                                    src={getChampionSquareAsset(champList, champion.championId)}
                                    alt={champion.championId}
                                    height="75"
                                    width="75"
                                />
                                <h3 className="w-2/4 text-left">{getChampionName(champList, champion.championId)}</h3>
                            </td>
                            <td className="number">
                                <div className="flex flex-row justify-center items-center">
                                    {champion.championLevel}
                                    <div
                                        className='rounded-3xl h-4 w-4 ml-2'
                                        style={{backgroundColor: color}}
                                    />
                                </div>
                            </td>
                            <td className="number">{champion.championPoints}</td>
                            <td className="number">{champion.championPointsUntilNextLevel}</td>
                        </tr>
                    )
                })}
                </tbody>
            </table>
        </div>
    )
}

export default MasteryTable