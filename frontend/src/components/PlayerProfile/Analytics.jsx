import {useEffect, useState} from "react";

const Analytics = () => {
    const [matchData, setMatchData] = useState({})
    const [retry, setRetry] = useState(false)

    useEffect(() => {
        const getMatchData = async () => {
            const res = await fetch("http://127.0.0.1:5000/match/get", {method: "GET", credentials: "include"})
            const data = await res.json()
            setMatchData(data)
        }
        getMatchData()
    }, [retry])

    function handleRetry() {
        setRetry(prev => !prev)
    }

    return (
        <div className="grid grid-cols-2 justify-items-center">
            <div>
                <h3>Cell 1</h3>
                <button onClick={handleRetry}>Retry</button>
            </div>
            <div>
                <h3>Cell 2</h3>
            </div>
            <div>
                <h3>Cell 3</h3>
            </div>
        </div>
    )
}

export default Analytics