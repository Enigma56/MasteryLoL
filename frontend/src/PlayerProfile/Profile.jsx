import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router";

import useAuth from "../hooks/useAuth.js"
import PlayerName from './PlayerName'
import MasteryTable from "./MasteryTable"
import Footer from '../Footer.jsx'

//TODO: Load everything then render profile
//TODO: Check to see if player exists before rendering & navigating to profile page
const Profile = () => {
    let navigate = useNavigate()
    const [searchParams, ] = useSearchParams()
    const { riotData: player, isLoading } = useAuth({name: searchParams.get("name"), tagline: searchParams.get("tag")})
    const [isMasteryList, setIsMasteryList] = useState(true)

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
        <div className="h-dvh">
            {Object.keys(player).length === 0 && isLoading === false ? (
                <div className="flex flex-col items-center">
                    <h1>
                        Player not found!
                    </h1>
                    <button type="submit" onClick={handleGoHome}>Go Home</button>
                </div>
            ) : (
                <>
                    <PlayerName name={player['game_name']} tag={player['tag_line']} isLoading={isLoading}/>
                    <div className="flex flex-row h-fit w-4/5 mx-auto">
                        <div className="flex flex-col h-full w-full">
                            <div className="flex flex-row justify-center">
                                <button
                                    id="masterylist"
                                    onClick={handleIsMasteryList}
                                    className={ isMasteryList ? "pr-2 underline" : "pr-2 hover:underline"}
                                >
                                    Mastery
                                </button>
                                <button
                                    id="masteryjourney"
                                    onClick={handleIsMasteryList}
                                    className={ !isMasteryList ? "pr-2 underline" : "pr-2 hover:underline"}
                                >
                                    Journey
                                </button>
                            </div>

                            {isMasteryList &&
                                <MasteryTable/>
                            }
                            {!isMasteryList &&
                                <div className="flex flex-row justify-center items-center h-full">
                                    <button className="rounded px-2 bg-hexmagic-4 h-fit">
                                        Start Journey
                                    </button>
                                </div>
                            }
                        </div>
                    </div>
                </>
            )}
            <Footer/>
        </div>
    )
}

export default Profile