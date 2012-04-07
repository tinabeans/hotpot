// from http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html
// Read a page's GET URL variables and return them as an associative array.
function getURLParams()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

Number.prototype.toPaddedString = function(len) {
	var s = String(this);
	while (s.length < len) { s = '0' + s; }
	return s;
};

Date.prototype.strftime = function(format) {
	var day = this.getDay(), month = this.getMonth();
	var hours = this.getHours(), minutes = this.getMinutes();
	function pad(num) { return num.toPaddedString(2); };
	return format.replace(/\%([aAbBcdDHIklmMpSTwyY])/g, function(part) {
		switch(part[1]) {
			case 'a': return ("Sun Mon Tue Wed Thu Fri Sat").split(' ')[day];
			case 'A': return ("Sunday Monday Tuesday Wednesday Thursday Friday Saturday").split(' ')[day];
			case 'b': return ("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec").split(' ')[month];
			case 'B': return ("January February March April May June July August September October November December").split(' ')[month];
			case 'c': return this.toString();
			case 'd': return this.getDate();
			case 'D': return pad(this.getDate());
			case 'H': return pad(hours);
			case 'I': return pad((hours + 11) % 12 + 1);
			case 'k': return hours;
			case 'l': return (hours + 11) % 12 + 1;
			case 'm': return pad(month + 1);
			case 'M': return pad(minutes);
			case 'p': return hours > 11 ? 'PM' : 'AM';
			case 'S': return pad(this.getSeconds());
			case 'T': return pad(hours) + ":" + pad(minutes) + ":" + pad(this.getSeconds());
			case 'w': return day;
			case 'y': return pad(this.getFullYear() % 100);
			case 'Y': return this.getFullYear();
		}
	}.bind(this));
};

function formatDatetimeLocale(tstamp, format) {
	return (new Date(tstamp * 1000)).strftime(format);
}
var TZ_NAME = (function getLocaleTzName() {
	var localeTimeStr = (new Date()).toLocaleTimeString();
	return localeTimeStr.substr(localeTimeStr.length - 3);
})();
