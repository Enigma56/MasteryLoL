const Home = () => {

    return (
        <div className="flex flex-col items-center">
            <h1>Mastery LoL</h1>
            <form name="profile" action="http://localhost:5173/account" method="POST" className="flex flex-col items-center">
                <div className="flex flex-row justify-center">
                    <label className="w-2/5">
                        <input id="profile" type="text" placeholder="Riot Name" maxLength="16" className="pl-2 w-full rounded outline outline-1 outline-hexmetal-3 placeholder:italic"/>
                    </label>
                    <label className="w-1/4">
                        <input id="tagline" type="text" placeholder="#Tagline" pattern="[A-Za-z0-9]{5}" maxLength="5" className="ml-0.5 pl-2 w-4/5 rounded outline outline-1 outline-hexmetal-3 placeholder:italic"/>
                    </label>
                </div>
                <button type="submit" className="mt-2 rounded bg-gradient-to-b from-hexmagic-4 to-hexmagic-3 w-1/3 text-amber-100">
                    Search
                </button>
            </form>
        </div>
    )
}

export default Home;