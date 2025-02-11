const Footer = () => {
    return (
        <footer className="flex flex-row justify-center max-h-fit mb-4">
            <div className="w-2/6">
                <p>
                    MasteryLoL is not endorsed by Riot Games and does not reflect
                    the views or opinions of Riot Games or anyone officially involved
                    in producing or managing Riot Games properties. Riot Games and all
                    associated properties are trademarks or registered trademarks of
                    Riot Games, Inc
                </p>
            </div>
            <div className="flex flex-col items-center w-1/6">
                <h5>SOCIALS</h5>
                <a>Something Here</a>
                <a>Another</a>
            </div>
            <div className="flex flex-col items-center w-1/6">
                <h5>LINKS</h5>
                <a>Privacy Policy</a>
                <a>Terms of Use?</a>
            </div>
        </footer>
    )
}

export default Footer