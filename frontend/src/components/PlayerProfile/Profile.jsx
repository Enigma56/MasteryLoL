import {useEffect, useState} from "react";
import { useSearchParams, useNavigate } from "react-router";

import useAuth from "../../hooks/useAuth.js"
import PlayerName from './PlayerName.jsx'
import Footer from '../Footer.jsx'
import Journey from "./Journey.jsx";

const Profile = () => {
    let navigate = useNavigate()
    const [searchParams, ] = useSearchParams()
    const { riotData: player, isLoading } = useAuth({name: searchParams.get("name"), tagline: searchParams.get("tag")})
    const [isJourneyView, setIsMasteryList] = useState(true)
    const [masteryScore, setMasteryScore] = useState(null)

    useEffect(() => {
        const getMastery = async () => {
            let res = await fetch("http://127.0.0.1:5000/mastery/sum", {method: "GET", credentials: 'include'})
            let data = await res.json()
            setMasteryScore(data)
        }
        getMastery()
    }, [])

    function handleIsJourneyView(e) {
        const id = e.target.id

        if (id === "masterylist") {
            setIsMasteryList(true)
        } else {
            setIsMasteryList(false)
        }
    }

    function handleGoHome() {
        navigate("/")
    }

    return (
        <div>
            <div className="flex flex-col">
                <div className="flex flex-row justify-center">
                    <button className="my-auto mr-10 h-10 w-8" onClick={handleGoHome}>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                             stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round"
                                  d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/>
                        </svg>
                    </button>
                    <PlayerName name={player['game_name']} tag={player['tag_line']} isLoading={isLoading}/>
                </div>
                <div className="flex flex-row mx-auto w-2/5 justify-center">
                    <h4>Total Mastery: {masteryScore}</h4>
                </div>
            </div>
            <div className="flex flex-col h-fit w-4/5 mx-auto">
            <div className="flex flex-row justify-center">
                    <button
                        id="masterylist"
                        onClick={handleIsJourneyView}
                        className={ isJourneyView ? "header-buttons pr-2 underline" : " header-buttons pr-2 hover:underline"}
                    >
                        Journey
                    </button>
                    <button
                        id="masteryjourney"
                        onClick={handleIsJourneyView}
                        className={ !isJourneyView ? "header-buttons pr-2 underline" : "header-buttons pr-2 hover:underline"}
                    >
                        Analytics
                    </button>
                </div>
                {isJourneyView ? <Journey/> : <p>Spaghetti</p> }
            </div>
            <Footer className="flex flex-col justify-center max-h-fit my-4"/>
        </div>
    )
}

export default Profile