import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import MinPriceChart from './components/MinPriceChart';
import './App.scss';

const theme = createTheme();

const App = () => {

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <h1>Tesla Tracker</h1>
        <div className='app__charts'>
          <MinPriceChart color='#BEE65F' initialYear={2024} />
          <MinPriceChart color='#A878F8' initialYear={2023} />
          <MinPriceChart color='#B2DBF7' initialYear={2022} />
          <MinPriceChart color='#2192D9' initialYear={2021} />
          <MinPriceChart color='#BEE65F' initialYear={2020} />
        </div>
      </div>
    </ThemeProvider>
  );
};

export default App;
