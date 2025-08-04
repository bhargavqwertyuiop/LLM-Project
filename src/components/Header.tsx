import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { Psychology, Analytics, Compare } from '@mui/icons-material';

const Header: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: <Psychology /> },
    { path: '/analysis', label: 'Analysis', icon: <Analytics /> },
    { path: '/compare', label: 'Compare', icon: <Compare /> },
  ];

  return (
    <AppBar position="static" elevation={2}>
      <Container maxWidth="xl">
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Psychology sx={{ mr: 2, fontSize: 32 }} />
            <Typography
              variant="h6"
              component={Link}
              to="/"
              sx={{
                flexGrow: 1,
                textDecoration: 'none',
                color: 'inherit',
                fontWeight: 'bold',
                fontSize: '1.5rem',
              }}
            >
              DocuMind
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', gap: 1 }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={Link}
                to={item.path}
                color="inherit"
                startIcon={item.icon}
                sx={{
                  borderRadius: 2,
                  px: 2,
                  backgroundColor:
                    location.pathname === item.path
                      ? 'rgba(255, 255, 255, 0.1)'
                      : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;