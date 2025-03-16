import {useEffect, useState} from "react";

export const useChampList = () => {
    const [champList, setChampList] = useState({}) //List of objects

    useEffect(() => {
        const fetchChamps = async () => {
            let res = await fetch(
                "http://127.0.0.1:5000/mastery/champs-by-id",
                {method: "GET", credentials: 'include'})

            let champs = await res.json()
            //console.log(champs)
            setChampList(champs)
        }

        fetchChamps().catch((err) => console.log(err))
    }, [])

    return champList
}