'use client'

import { APISignOut } from "@/api/authentication/signout";
import { APIUserGet } from "@/api/user/get";
import { AppBar, Toolbar, Typography, CircularProgress, Button, Popover, Link, Modal } from "@mui/material";
import { redirect } from "next/navigation";
import MicrosoftIcon from '@mui/icons-material/Microsoft';
import WebIcon from '@mui/icons-material/Web';
import AndroidIcon from '@mui/icons-material/Android';
import AppleIcon from '@mui/icons-material/Apple';
import TerminalIcon from '@mui/icons-material/Terminal';
import DevicesIcon from '@mui/icons-material/Devices';
import { useEffect, useState } from "react";

function NavBar() {
    const [token, setToken] = useState('');
    const [anchorEl, setAnchorEl] = useState(null);
    const [response, setResponse] = useState(null);
    const [openModal, setOpenModal] = useState(false);
    const [selectedToken, setSelectedToken] = useState(null);
    
    const handleClick = (event: any, token: any) => {
      setAnchorEl(event.currentTarget);
      setSelectedToken(token);
    };

    const handleClose = () => {
      setAnchorEl(null);
      setSelectedToken(null);
    };

    const handleOpenModal = () => {
      setOpenModal(true);
      handleClose();
    };

    const handleCloseModal = () => {
      setOpenModal(false);
    };

    const defineDeviceIcon = (deviceName: string)=>{
      let lowercaseString = deviceName.toLowerCase();

      if (lowercaseString.includes("web")) {
          return <WebIcon/>
      } else if (lowercaseString.includes("windows")) {
          return <MicrosoftIcon/>;
      } else if (lowercaseString.includes("linux")) {
          return <TerminalIcon/>
      } else if (lowercaseString.includes("android")) {
          return <AndroidIcon/>
      } else if (lowercaseString.includes("ios")) {
          return <AppleIcon/>
      } else {
          return <DevicesIcon/>
      }
    }

    const handleLogout = async (tokenId: string) => {
      try {
        let api = new APISignOut(token, tokenId);
        let response = await api.execute();
        console.log("Hello");
        if (response.status === 200) {
          console.log(response.status);
          // Update the state with the filtered tokens
          setResponse((prevResponse) => ({
            ...prevResponse,
            data: {
              ...prevResponse.data,
              tokens: prevResponse.data.tokens.filter((t: any) => t.id !== tokenId),
            },
          }));
        }
      } catch (error: any) {
        return;
      }
    };

    const fetchData = async () => {
        try {
            const secureDataString = localStorage.getItem('secure');
            if (secureDataString !== null) {
                let secureData = JSON.parse(secureDataString);
                const currentToken = secureData ? secureData.token : '400';
                setToken(currentToken);
                let apiSignIn = new APIUserGet(currentToken);
                const apiResponse = await apiSignIn.execute();
                setResponse(apiResponse);
            } else {
                console.error('secureDataString is null');
                return;
            }
        } catch (error: any) {
            console.error('API error:', error);
            setResponse(error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (response && response.status !== 200) {
            redirect('/auth/signin');
        }
    }, [response]);

    if (!response) {
        return (
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6">Loading...</Typography>
                    <CircularProgress color="inherit" size={20} style={{ marginLeft: '10px' }} />
                </Toolbar>
            </AppBar>
        );
    }

    if (!response || !response.data) {
        return (
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6">Loading...</Typography>
              <CircularProgress color="inherit" size={20} style={{ marginLeft: '10px' }} />
            </Toolbar>
          </AppBar>
        );
      }
      
      const { information } = response.data;

      const open = Boolean(anchorEl);
      const id = open ? 'simple-popover' : undefined;

      return (
        <>
            <AppBar position="static">
                <Toolbar>
                    <div style={{ display: 'flex', marginRight: 'auto'}}>
                        <Link href="/">
                        <Typography variant="h6" style={{ cursor: 'pointer',  color: 'white' }}>
                            MindfulGuard
                        </Typography>
                        </Link>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', marginLeft: 'auto' }}>
                        <div>
                            <Typography variant="h6" onClick={handleClick} style={{ cursor: 'pointer' }}>
                                {information?.username}
                            </Typography>
                            <Popover id={id} open={open} anchorEl={anchorEl} onClose={handleClose} anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }} transformOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}>
                                <div style={{ display: 'flex', flexDirection: 'column', padding: '10px' }}>
                                    <Button onClick={handleOpenModal}>Logout</Button>
                                </div>
                            </Popover>

                            <style jsx>{`
                              .scroll-container {
                                overflow-y: auto;
                                max-height: 80vh;
                                padding-right: 15px;
                              }

                              .scroll-container::-webkit-scrollbar {
                                width: 10px;
                              }

                              .scroll-container::-webkit-scrollbar-thumb {
                                background-color: #1976D2;
                                border-radius: 5px;
                              }

                              .scroll-container::-webkit-scrollbar-track {
                                background-color: #f1f1f1;
                              }
                            `}</style>

                            <Modal open={openModal} onClose={handleCloseModal}>
                                <div className="scroll-container" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)', maxHeight: '80vh', overflowY: 'auto' }}>
                                    <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>Tokens Information</h2>
                                    {response && response.data && response.data.tokens && response.data.tokens.map((token: any) => (
                                      <div key={token.id} style={{ marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
                                          <p style={{ fontWeight: 'bold', marginBottom: '5px' }}>Token ID: {token.id}</p>
                                          <p>Device: {token.device} {defineDeviceIcon(token.device)}</p>
                                          <p>Created at: {new Date(token.created_at * 1000).toLocaleString()}</p>
                                          <p>Updated at: {new Date(token.updated_at * 1000).toLocaleString()}</p>
                                          <p>Last IP: {token.last_ip}</p>
                                          <p>Expiration: {new Date(token.expiration * 1000).toLocaleString()}</p>
                                          <Button onClick={() => handleLogout(token.id)}>Terminate Session</Button>
                                      </div>
                                  ))}

                                    <Button onClick={handleCloseModal} style={{ marginTop: '10px' }}>Close</Button>
                                </div>
                            </Modal>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            {/* Here you can add any additional content on the right side */}
                        </div>
                    </div>
                </Toolbar>
            </AppBar>
        </>
    );
}

export default NavBar