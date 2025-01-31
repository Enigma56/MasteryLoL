import {useEffect, useState} from "react";
import {getChampionName, getChampionSquareAsset} from "../../utils/dataDragonAssets.js";

const MasteryTable = () => {
    const [mastery, setMastery] = useState([])
    useEffect(() => {
        const getTopMastery = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/top", {method: "GET", credentials: 'include'})
            const data = await res.json()
            setMastery(data)
            console.log(data)
        }
        getTopMastery()
    }, [])

    return (
        <>
            <button className="mt-4">
                Get Mastery
            </button>
            <table>
                <thead>
                    <tr >
                        <th>Champion</th>
                        <th>Level</th>
                        <th>Points</th>
                        <th>Points to Next Level</th>
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
                            <td>{champion.championLevel}</td>
                            <td>{champion.championPoints}</td>
                            <td>{champion.championPointsUntilNextLevel}</td>
                        </tr>
                    )
                })}
                </tbody>
            </table>
        </>
    )
}

export default MasteryTable