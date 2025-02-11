import {useEffect, useState} from "react";
import {getChampionName, getChampionSquareAsset} from "../../utils/dataDragonAssets.js";

const MasteryTable = () => {
    const [mastery, setMastery] = useState([])
    useEffect(() => {
        const getTopMastery = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/all", {method: "GET", credentials: 'include'})
            const data = await res.json()
            setMastery(data)
            console.log(data)
        }
        getTopMastery()
    }, [])

    function handleChampionLevelPng(championLevel) {
        let color
        switch (championLevel) {
            case 1:
                color = "bg-[#A09B8C]"
                break
            case 2:
                color = "bg-[#A09B8C]"
                break
            case 3:
                color = "bg-[#A09B8C]"
                break
            case 4:
                color = "bg-[#A09B8C]"
                break
            case 5:
                color = "bg-[#A09B8C]"
                break
            case 6:
                color = "bg-[#A09B8C]"
                break
            case 7:
                color = "bg-[#A09B8C]"
                break
            case 8:
                color = "bg-[#A09B8C]"
                break
            case 9:
                color = "bg-[#A09B8C]"
                break
            default:
                color = "bg-[#A09B8C]"
                break
        }

        return `${color} rounded-3xl h-4 w-4 ml-2`
    }

    return (
        <table className="my-4">
            <thead>
                <tr className="text-hexmetal-2 underline">
                    <th><h3>CHAMPION</h3></th>
                    <th><h3>LEVEL</h3></th>
                    <th><h3>POINTS</h3></th>
                    <th><h3>TO NEXT LEVEL</h3></th>
                </tr>
            </thead>
            <tbody>
            {mastery.map((champion, idx) => {
                return (
                    <tr key={idx} className="text-center">
                        <td className="flex flex-row justify-around">
                            <img
                                src={getChampionSquareAsset(champion.championId)}
                                alt={champion.championId}
                                height="75"
                                width="75"
                            />
                            <h3 className="w-1/4 text-left">{getChampionName(champion.championId)}</h3>
                        </td>
                        <td className="number">
                            <div className="flex flex-row justify-center items-center">
                                {champion.championLevel}
                                <div className="bg-[#A09B8C] rounded-3xl h-4 w-4 ml-2"/>
                            </div>
                        </td>
                        <td className="number">{champion.championPoints}</td>
                        <td className="number">{champion.championPointsUntilNextLevel}</td>
                    </tr>
                )
            })}
            </tbody>
        </table>
    )
}

export default MasteryTable