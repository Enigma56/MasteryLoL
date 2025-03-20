import {useEffect, useState} from "react";
import MasteryTable from "./MasteryTable.jsx";

const Journey = () => {
    const [journeyStarted, setJourneyStarted] = useState(false)
    const [masteryPoints, setMasteryPoints] = useState(null)


    useEffect(() => {
        const startJourney = async () => {
            await fetch("http://127.0.0.1:5000/journey/start", {method: "POST", credentials: "include"})
        }

        const getPoints = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/points", {method: "GET", credentials: 'include'})
            let data = await res.json()
            setMasteryPoints(data)
        }

        if (journeyStarted) {
            startJourney().then(() => {getPoints()})
        }
    }, [journeyStarted])

    const handleStartJourney = () => {
        setJourneyStarted(true)
    }

    return (
        <>
            {!journeyStarted &&
            <div className="flex flex-row justify-center items-center h-full">
                <button
                    className="rounded px-2 bg-hexmagic-4 h-fit"
                    onClick={handleStartJourney}>
                    Start Journey
                </button>
            </div>
            }

            {journeyStarted &&
                <>
                    <div className="flex flex-row mx-auto w-2/5 justify-between">
                        <h4>Points: {masteryPoints} of 1,000,000</h4>
                    </div>
                    <MasteryTable/>
                </>
            }
        </>
    )
}

export default Journey