import {useEffect, useState} from "react";
import { useSearchParams, useNavigate } from "react-router";

import useAuth from "../../hooks/useAuth.js"
import PlayerName from './PlayerName.jsx'
import MasteryTable from "./MasteryTable.jsx"
import Footer from '../Footer.jsx'
import Journey from "./Journey.jsx";

//TODO: Load everything then render profile
//TODO: Check to see if player exists before rendering & navigating to profile page
const Profile = () => {
    let navigate = useNavigate()
    const [searchParams, ] = useSearchParams()
    const { riotData: player, isLoading } = useAuth({name: searchParams.get("name"), tagline: searchParams.get("tag")})
    const [isMasteryList, setIsMasteryList] = useState(true)
    const [masteryPoints, setMasteryPoints] = useState(0)

    useEffect(() => {
        const getMastery = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/sum", {method: "GET", credentials: 'include'})
            let data = await res.json()
            setMasteryPoints(data)
        }
        getMastery()
    }, [])
    function handleIsMasteryList(e) {
        const id = e.target.id

        if (id === "masterylist") {
            setIsMasteryList(true)
        } else {
            setIsMasteryList(false)
        }
    }

    function handleGoHome(e) {
        navigate("/")
    }

    //TODO: Move button style into a group to apply to both buttons
    return (
        <div>
            <div className="flex flex-col">
                <div className="flex flex-row justify-center">
                    <button className="pr-4" onClick={handleGoHome}>X</button>
                    <PlayerName name={player['game_name']} tag={player['tag_line']} isLoading={isLoading}/>
                </div>
                <div className="flex flex-row mx-auto w-2/5 justify-between">
                    <h4>Total Mastery: {masteryPoints}</h4>
                    <h4>Points: 0 of 1,000,000</h4>
                </div>
            </div>
            <div className="flex flex-col h-fit w-4/5 mx-auto">
                <div className="flex flex-row justify-center">
                    <button
                        id="masterylist"
                        onClick={handleIsMasteryList}
                        className={ isMasteryList ? "header-buttons pr-2 underline" : " header-buttons pr-2 hover:underline"}
                    >
                        Mastery
                    </button>
                    <button
                        id="masteryjourney"
                        onClick={handleIsMasteryList}
                        className={ !isMasteryList ? "header-buttons pr-2 underline" : "header-buttons pr-2 hover:underline"}
                    >
                        Journey
                    </button>
                </div>
                {isMasteryList ? <MasteryTable/> : <Journey/> }
            </div>
            <Footer/>
        </div>
    )
}

export default Profile