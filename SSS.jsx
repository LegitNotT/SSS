import React, { useState, useEffect } from 'react';
import { Calculator, DollarSign, Settings, History, Plus, Trash2, Edit2 } from 'lucide-react';

const JewelryPricingApp = () => {
  const [currentTab, setCurrentTab] = useState('calculator');
  const [showInitialInput, setShowInitialInput] = useState(true);
  
  const [prices, setPrices] = useState({
    goldWithoutGST: '', goldWithGST: '', silverWithoutGST: '', silverWithGST: ''
  });
  
  const [weight, setWeight] = useState('');
  const [material, setMaterial] = useState('gold');
  const [includeGST, setIncludeGST] = useState(true);
  const [selectedWage, setSelectedWage] = useState({ id: 'default', material: 'Default', rate: 1000 });
  const [wagesList, setWagesList] = useState([
    { id: 'default', srNo: 1, material: 'Default', rate: 1000 }
  ]);
  const [calculationPreview, setCalculationPreview] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const lastInputDate = localStorage.getItem('lastInputDate');
    const lastInputTime = localStorage.getItem('lastInputTime');
    const today = new Date();
    const currentHour = today.getHours();
    const todayString = today.toDateString();
    
    // Check if it's first run, different day, or after 8 AM if not already input today after 8 AM
    const shouldShowInput = !lastInputDate || 
                           lastInputDate !== todayString || 
                           (currentHour >= 8 && (!lastInputTime || 
                            new Date(lastInputTime).toDateString() !== todayString || 
                            new Date(lastInputTime).getHours() < 8));
    
    if (shouldShowInput) {
      setShowInitialInput(true);
    } else {
      const savedPrices = localStorage.getItem('dailyPrices');
      if (savedPrices) {
        setPrices(JSON.parse(savedPrices));
        setShowInitialInput(false);
      }
    }
    
    const savedWages = localStorage.getItem('wagesList');
    const savedHistory = localStorage.getItem('history');
    
    if (savedWages) setWagesList(JSON.parse(savedWages));
    if (savedHistory) setHistory(JSON.parse(savedHistory));
  }, []);

  // Update calculation preview whenever inputs change
  useEffect(() => {
    if (weight && prices.goldWithoutGST) {
      const weightNum = parseFloat(weight) || 0;
      const pricePerGram = material === 'gold' 
        ? (includeGST ? parseFloat(prices.goldWithGST) : parseFloat(prices.goldWithoutGST))
        : (includeGST ? parseFloat(prices.silverWithGST) : parseFloat(prices.silverWithoutGST));
      const total = weightNum * pricePerGram * selectedWage.rate;
      setCalculationPreview(`${weightNum}g × ₹${pricePerGram}/g × ${selectedWage.rate} = ₹${total.toLocaleString()}`);
    } else {
      setCalculationPreview('');
    }
  }, [weight, material, includeGST, selectedWage, prices]);
  
  const handleInitialSubmit = () => {
    if (prices.goldWithoutGST && prices.goldWithGST && prices.silverWithoutGST && prices.silverWithGST) {
      const now = new Date();
      localStorage.setItem('dailyPrices', JSON.stringify(prices));
      localStorage.setItem('lastInputDate', now.toDateString());
      localStorage.setItem('lastInputTime', now.toISOString());
      setShowInitialInput(false);
    }
  };
  
  const calculate = () => {
    if (!weight || !prices.goldWithoutGST) return;
    
    const weightNum = parseFloat(weight);
    const pricePerGram = material === 'gold' 
      ? (includeGST ? parseFloat(prices.goldWithGST) : parseFloat(prices.goldWithoutGST))
      : (includeGST ? parseFloat(prices.silverWithGST) : parseFloat(prices.silverWithoutGST));
    
    const total = weightNum * pricePerGram * selectedWage.rate;
    setResult({ weight: weightNum, pricePerGram, wages: selectedWage.rate, total, material, includeGST });
  };
  
  const saveToHistory = () => {
    if (result) {
      const newEntry = { ...result, timestamp: new Date().toLocaleString(), id: Date.now() };
      const newHistory = [newEntry, ...history];
      setHistory(newHistory);
      localStorage.setItem('history', JSON.stringify(newHistory));
      setWeight(''); setResult(null);
    }
  };

  const addWageEntry = () => {
    const newEntry = {
      id: Date.now(),
      srNo: wagesList.length + 1,
      material: `Item ${wagesList.length + 1}`,
      rate: 1000
    };
    const updatedWages = [...wagesList, newEntry];
    setWagesList(updatedWages);
    localStorage.setItem('wagesList', JSON.stringify(updatedWages));
  };

  const deleteWageEntry = (id) => {
    if (wagesList.length === 1) return; // Don't delete if it's the last item
    
    const updatedWages = wagesList.filter(wage => wage.id !== id);
    // Update serial numbers
    const reorderedWages = updatedWages.map((wage, index) => ({ ...wage, srNo: index + 1 }));
    
    setWagesList(reorderedWages);
    localStorage.setItem('wagesList', JSON.stringify(reorderedWages));
    
    // If deleted item was selected, select the first one
    if (selectedWage.id === id) {
      setSelectedWage(reorderedWages[0]);
    }
  };

  const updateWageEntry = (id, field, value) => {
    const updatedWages = wagesList.map(wage => 
      wage.id === id ? { ...wage, [field]: value } : wage
    );
    setWagesList(updatedWages);
    localStorage.setItem('wagesList', JSON.stringify(updatedWages));
    if (selectedWage.id === id) {
      setSelectedWage({ ...selectedWage, [field]: value });
    }
  };

  const selectWage = (wage) => {
    setSelectedWage(wage);
  };

  const updatePrice = (key, value) => {
    const updatedPrices = { ...prices, [key]: value };
    setPrices(updatedPrices);
    localStorage.setItem('dailyPrices', JSON.stringify(updatedPrices));
  };

  if (showInitialInput) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-600 to-cyan-700 flex items-center justify-center p-4">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-6">
          <h1 className="text-2xl font-bold text-center mb-8 text-teal-800">Good Morning!</h1>
          <div className="space-y-4">
            {[
              { key: 'goldWithoutGST', label: 'Gold Price (without GST)' },
              { key: 'goldWithGST', label: 'Gold Price (with GST)' },
              { key: 'silverWithoutGST', label: 'Silver Price (without GST)' },
              { key: 'silverWithGST', label: 'Silver Price (with GST)' }
            ].map(({ key, label }) => (
              <div key={key}>
                <label className="block text-sm font-medium mb-2 text-gray-700">{label}</label>
                <input
                  type="number"
                  value={prices[key]}
                  onChange={(e) => setPrices({...prices, [key]: e.target.value})}
                  className="w-full p-3 rounded-xl border border-gray-200 bg-gray-50 focus:ring-2 focus:ring-teal-500"
                  placeholder="₹ per gram"
                />
              </div>
            ))}
            <button onClick={handleInitialSubmit} className="w-full bg-teal-700 text-white p-4 rounded-xl font-semibold mt-6 hover:bg-teal-800">
              Continue
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-600 to-cyan-700">
      {/* Header */}
      <div className="bg-teal-700 bg-opacity-90 backdrop-blur-sm sticky top-0 z-50">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold text-white">SSS</h1>
            <span className="text-sm text-teal-200">Jewelry Calculator</span>
          </div>
        </div>
        
        {/* Tab Navigation */}
        <div className="flex bg-teal-600 bg-opacity-50">
          {[
            { id: 'calculator', icon: Calculator, label: 'Calculator' },
            { id: 'wages', icon: Settings, label: 'Wages' },
            { id: 'prices', icon: DollarSign, label: 'Prices' },
            { id: 'history', icon: History, label: 'History' }
          ].map(({ id, icon: Icon, label }) => (
            <button
              key={id}
              onClick={() => setCurrentTab(id)}
              className={`flex-1 py-3 px-2 text-sm font-medium flex items-center justify-center space-x-2 ${
                currentTab === id 
                  ? 'bg-white bg-opacity-20 text-white border-b-2 border-white' 
                  : 'text-teal-200 hover:text-white'
              }`}
            >
              <Icon size={16} />
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content Area */}
      <div className="p-4">
        
        {/* Calculator Tab */}
        {currentTab === 'calculator' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6 mb-4">
              {/* Material Selection */}
              <div className="flex justify-center mb-4">
                <div className="bg-gray-100 rounded-xl p-1 flex">
                  {['gold', 'silver'].map(mat => (
                    <button
                      key={mat}
                      onClick={() => setMaterial(mat)}
                      className={`px-6 py-3 rounded-lg font-medium transition-all ${
                        material === mat
                          ? (mat === 'gold' ? 'bg-yellow-500' : 'bg-gray-500') + ' text-white shadow-lg'
                          : 'text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {mat.charAt(0).toUpperCase() + mat.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Result Widget - Moved to top */}
              {result && (
                <div className="mb-4 p-4 bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl border border-teal-200">
                  <div className="text-center">
                    <p className="text-sm text-teal-600 mb-1">Calculated Price</p>
                    <div className="text-3xl font-bold text-teal-700">₹{result.total.toLocaleString()}</div>
                  </div>
                </div>
              )}

              {/* Weight Input */}
              <div className="mb-4">
                <p className="text-sm text-gray-500 text-center mb-2">Weight (grams)</p>
                <input
                  type="number"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  className="w-full p-4 rounded-xl bg-gray-100 text-3xl text-center font-mono focus:ring-2 focus:ring-teal-500"
                  placeholder="0"
                />
              </div>

              {/* GST Toggle */}
              <div className="flex justify-between items-center mb-6 p-4 bg-gray-50 rounded-xl">
                <span className="font-medium">Include GST</span>
                <button
                  onClick={() => setIncludeGST(!includeGST)}
                  className={`w-12 h-6 rounded-full p-1 transition-colors ${includeGST ? 'bg-teal-600' : 'bg-gray-300'}`}
                >
                  <div className={`w-4 h-4 rounded-full bg-white transition-transform ${includeGST ? 'translate-x-6' : 'translate-x-0'}`} />
                </button>
              </div>

              {/* Number Pad */}
              <div className="grid grid-cols-3 gap-3 mb-6">
                {[1,2,3,4,5,6,7,8,9].map(num => (
                  <button
                    key={num}
                    onClick={() => setWeight(prev => prev === '0' ? num.toString() : prev + num.toString())}
                    className="aspect-square rounded-xl bg-gray-50 hover:bg-gray-100 text-xl font-medium transition-colors shadow-sm"
                  >
                    {num}
                  </button>
                ))}
                <button
                  onClick={() => setWeight(prev => prev.includes('.') ? prev : prev + '.')}
                  className="aspect-square rounded-xl bg-gray-50 hover:bg-gray-100 text-xl font-medium"
                >
                  .
                </button>
                <button
                  onClick={() => setWeight(prev => prev === '0' ? '0' : prev + '0')}
                  className="aspect-square rounded-xl bg-gray-50 hover:bg-gray-100 text-xl font-medium"
                >
                  0
                </button>
                <button
                  onClick={() => setWeight(prev => prev.length > 1 ? prev.slice(0, -1) : '')}
                  className="aspect-square rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-lg font-medium"
                >
                  ⌫
                </button>
              </div>

              {/* Calculate Button */}
              <button
                onClick={calculate}
                className="w-full bg-gradient-to-r from-pink-500 to-rose-500 text-white p-4 rounded-xl font-semibold text-lg mb-4 hover:from-pink-600 hover:to-rose-600 transition-all"
              >
                Calculate
              </button>

              {/* Calculation Preview - Moved to bottom */}
              {calculationPreview && (
                <div className="p-3 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-600 text-center font-mono">{calculationPreview}</p>
                </div>
              )}
            </div>

            {/* Action Buttons - Only show when result exists */}
            {result && (
              <div className="bg-white rounded-2xl shadow-xl p-4">
                <div className="flex gap-3">
                  <button onClick={() => {setWeight(''); setResult(null);}} className="flex-1 bg-red-500 text-white p-3 rounded-xl">
                    Clear
                  </button>
                  <button onClick={saveToHistory} className="flex-1 bg-green-500 text-white p-3 rounded-xl">
                    Save
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Wages Tab */}
        {currentTab === 'wages' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">Making Charges</h2>
                <button onClick={addWageEntry} className="bg-teal-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-teal-800">
                  <Plus size={16} />
                </button>
              </div>
              
              <div className="space-y-3">
                <div className="grid grid-cols-4 gap-2 text-sm font-medium text-gray-600 pb-2 border-b">
                  <span>Sr.</span>
                  <span>Material</span>
                  <span>Rate</span>
                  <span>Del</span>
                </div>
                
                {wagesList.map((wage) => (
                  <div 
                    key={wage.id} 
                    className={`grid grid-cols-4 gap-2 p-3 rounded-xl cursor-pointer transition-all ${
                      selectedWage.id === wage.id ? 'bg-teal-100 border-2 border-teal-300' : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                    onClick={() => selectWage(wage)}
                  >
                    <span className="text-sm">{wage.srNo}</span>
                    <input
                      type="text"
                      value={wage.material}
                      onChange={(e) => updateWageEntry(wage.id, 'material', e.target.value)}
                      className="text-sm bg-transparent border-none focus:outline-none"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <input
                      type="number"
                      value={wage.rate}
                      onChange={(e) => updateWageEntry(wage.id, 'rate', Number(e.target.value))}
                      className="text-sm bg-transparent border-none focus:outline-none w-16"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteWageEntry(wage.id);
                      }}
                      className="text-red-500 hover:text-red-700 flex justify-center items-center"
                      disabled={wagesList.length === 1}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                ))}
              </div>
              
              {selectedWage && (
                <div className="mt-6 p-4 bg-teal-50 rounded-xl">
                  <p className="text-sm text-teal-700">Selected: <span className="font-medium">{selectedWage.material}</span> (Rate: {selectedWage.rate}x)</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Prices Tab */}
        {currentTab === 'prices' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-xl font-bold mb-6 text-center">Current Prices</h2>
              
              <div className="space-y-4">
                {[
                  { key: 'goldWithoutGST', label: 'Gold (No GST)', color: 'yellow' },
                  { key: 'goldWithGST', label: 'Gold (With GST)', color: 'yellow' },
                  { key: 'silverWithoutGST', label: 'Silver (No GST)', color: 'gray' },
                  { key: 'silverWithGST', label: 'Silver (With GST)', color: 'gray' }
                ].map(({ key, label, color }) => (
                  <div key={key} className={`flex items-center space-x-3 p-4 bg-${color}-50 rounded-xl`}>
                    <div className={`w-3 h-3 bg-${color}-500 rounded-full`}></div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-800">{label}</p>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">₹</span>
                        <input
                          type="number"
                          value={prices[key]}
                          onChange={(e) => updatePrice(key, e.target.value)}
                          className="text-xl font-bold bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-teal-500 rounded px-2"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <button
                onClick={() => setShowInitialInput(true)}
                className="w-full bg-teal-700 text-white p-4 rounded-xl font-medium mt-6 hover:bg-teal-800"
              >
                Reset Daily Prices
              </button>
            </div>
          </div>
        )}

        {/* History Tab */}
        {currentTab === 'history' && (
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">History</h2>
                {history.length > 0 && (
                  <button onClick={() => {setHistory([]); localStorage.setItem('history', '[]');}} className="text-red-600 text-sm">
                    Clear All
                  </button>
                )}
              </div>
              
              {history.length === 0 ? (
                <div className="text-center py-8 text-gray-400">
                  <History size={48} className="mx-auto mb-2 opacity-50" />
                  <p>No calculations saved</p>
                </div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {history.map((entry) => (
                    <div key={entry.id} className="p-4 bg-gray-50 rounded-xl">
                      <div className="flex justify-between items-start mb-2">
                        <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                          entry.material === 'gold' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {entry.material.toUpperCase()} {entry.weight}g
                        </span>
                        <span className="text-xl font-bold">₹{entry.total.toLocaleString()}</span>
                      </div>
                      <p className="text-xs text-gray-500">{entry.timestamp}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
};

export default JewelryPricingApp;s