function getDepartmentFilters() {
  console.log("Preparing departments JSON");
    
  var activeDepartments = [];
    
  departments = document.getElementsByClassName("departments");
  
  for (var i = 0; i < departments.length; i++) {
    if (departments[i].checked) {
        activeDepartments.push(departments[i].value);
    }
  }
  
  return activeDepartments;
};

function getPayFilters() {
  console.log("Preparing pay JSON");
    
  var activePay = [];
    
  pay = document.getElementsByClassName("pay");
  
  for (var i = 0; i < pay.length; i++) {
    if (pay[i].checked) {
        activePay.push(pay[i].value);
    }
  }
  
  console.log(activePay);
  
  return activePay;
}

function getLocationFilters() {
  console.log("Preparing locations JSON");
    
  var activeLocations = [];
    
  locations = document.getElementsByClassName("locations");
  
  for (var i = 0; i < locations.length; i++) {
    if (locations[i].checked) {
        activeLocations.push(locations[i].value);
    }
  }
  
  return activeLocations;
}

function getSeasonFilters() {
  console.log("Preparing seasons JSON");
    
  var activeSeasons = [];
    
  seasons = document.getElementsByClassName("seasons");
  
  for (var i = 0; i < seasons.length; i++) {
    if (seasons[i].checked) {
        activeSeasons.push(seasons[i].value);
    }
  }
  
  return activeSeasons;
}

function getInstituteWideResearchCenters() {
    console.log("Preparing institute wide research centers JSON");
        
    var activeCenters = [];
        
    centers = document.getElementsByClassName("institute-wide-research-centers");
    
    for (var i = 0; i < centers.length; i++) {
        if (centers[i].checked) {
            activeCenters.push(centers[i].value);
        }
    }
    
    return activeCenters;
    
}

function getOtherResearchCenters() {
    console.log("Preparing other research centers JSON");
        
    var activeCenters = [];
        
    centers = document.getElementsByClassName("other-research-centers");
    
    for (var i = 0; i < centers.length; i++) {
        if (centers[i].checked) {
            activeCenters.push(centers[i].value);
        }
    }
    
    return activeCenters;
}

function prepareFilterJSON() {
    var activeDepartments = getDepartmentFilters();
    var activePay = getPayFilters();
    var activeLocations = getLocationFilters();
    var activeSeasons = getSeasonFilters();
    
    var filterJSON = {
        "departments": activeDepartments,
        "pay": activePay,
        "locations": activeLocations,
        "seasons": activeSeasons
    };
    
    return filterJSON;
}