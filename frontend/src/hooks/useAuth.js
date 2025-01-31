import {useEffect, useState} from "react";

//TODO: Get a POST request to run before a GET request
//TODO: Only run once
/**
 * Retrieves user data from server
 * @param {String} name
 * @param {String} tagline
 * @returns {Object} riotUser & isLoading
 */
const useAuth = ({name, tagline}) => {
    const url = `http://127.0.0.1:5000/account/user?name=${name}&tag=${tagline}`
    const [riotData, setRiotData] = useState({})
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchRiotUser = async () => {
            setIsLoading(true)
            try{
                let res = await fetch(url, {method: "GET", credentials: 'include'})

                if (res.status >= 400) {
                    let postRes = await fetch(url, {method: "POST", credentials: 'include'}).catch(error => console.log(error))
                    const data = await postRes.json()
                    //if (postRes.status = 400) {}
                    setRiotData(data)
                } else {
                    const data = await res.json()
                    setRiotData(data)
                }
            } catch (e) {
                console.error(e)
            } finally {
                setIsLoading(false)
            }
        }
        fetchRiotUser().catch(e => console.error(e))
    }, [name, tagline, url])

    return { riotData, isLoading }
}

export default useAuth