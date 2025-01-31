import { useNavigate } from "react-router"
import {useState, useEffect, useRef} from "react"
import Footer from "./Footer.jsx";

//TODO: Validate whether user exists before navigation
const Home = () => {
    let navigate = useNavigate()
    const [riotUser, setRiotUser] = useState({name: "", tagline: ""})
    const [isNotQueryableUser, setIsNotQueryableUser] = useState(true)
    const formRef = useRef(null)

    //Grabs id of element and conditionally changes the field
    function handleInputChange(e) {
        const { id, value } = e.target
        const updatedField = id === "profile" ? "name" : "tagline"

        setRiotUser( prevRiotUser => {
            const newRiotUser = {...prevRiotUser, [updatedField]: value}
            setIsNotQueryableUser(newRiotUser.name === "" || newRiotUser.tagline === "")
            return newRiotUser
        })
    }

    return (
        <>
            <div className="flex flex-col items-center">
                <h1>Mastery LoL</h1>
                <form ref={formRef} name="profile" className="flex flex-col items-center" onSubmit={(e) => {
                    e.preventDefault()
                    navigate(`/profile?name=${riotUser.name}&tag=${riotUser.tagline}`)
                }}>
                    <div className="flex flex-row justify-center">
                        <label className="w-2/5">
                            <input id="profile" type="text" placeholder="Riot Name" pattern="[A-Za-z0-9\s]{1,17}" maxLength="16" className="pl-2 w-full rounded outline outline-1 outline-hexmetal-3 placeholder:italic"
                            onChange={handleInputChange}/>
                        </label>
                        <label className="w-1/4">
                            <input id="tagline" type="text" placeholder="#Tagline" pattern="[A-Za-z0-9]{1,5}" maxLength="5" className="ml-0.5 pl-2 w-4/5 rounded outline outline-1 outline-hexmetal-3 placeholder:italic"
                            onChange={handleInputChange}/>
                        </label>
                    </div>
                    <button type="submit" className="mt-2 rounded bg-gradient-to-b from-hexmagic-4 to-hexmagic-3 w-1/3 text-amber-100" disabled={isNotQueryableUser}>
                        Search
                    </button>
                </form>
            </div>
            <Footer/>
        </>
    )
}

export default Home;