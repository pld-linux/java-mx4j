#
# TODO:
#		- update to 2.0.1
#
Summary:	Open source implementation of JMX Java API
Summary(pl):	Implementacja API Javy JMX z otwartymi ¼ród³ami
Name:		mx4j
Version:	1.1.1
Release:	0.1
Epoch:		0
License:	Apache License
Group:		Development/Languages/Java
# File http://dl.sf.net/%{name}/%{name}-%{version}.tar.gz have unusable sources!
# So, we'll use a snap from jpp (probably a cvs snapshot).
Source0:	%{name}-%{version}jpp.tar.gz
URL:		http://mx4j.sf.net/
BuildRequires:	jakarta-ant
BuildRequires:	jaf
BuildRequires:	javamail >= 1.2
BuildRequires:	jython >= 2.1
BuildRequires:	jakarta-log4j >= 1.2.7
BuildRequires:	jakarta-commons-logging >= 1.0.1
BuildRequires:	xml-commons
BuildRequires:	jakarta-bcel >= 5.0
BuildRequires:	jsse >= 1.0.2
BuildRequires:	jce >= 1.2.2
BuildRequires:	junit >= 3.8
Requires:	jre
Provides:	jmxri
Obsoletes:	openjmx
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenJMX is an open source implementation of the Java(TM) Management
Extensions (JMX).

%description -l pl
OpenJMX to implementacja standardu JMX (Java(TM) Management
Extensions) z otwartymi ¼ród³ami.

%prep
%setup -q -n %{name}
find lib -type f ! -name "xdoclet*.jar" ! -name "docbook*.*" ! -name "xjavadoc*.jar" -exec rm -f \{\} \;

%build
CLASSPATH=%{_javadir}/activation.jar
CLASSPATH=$CLASSPATH:%{_javadir}/mailapi.jar
CLASSPATH=$CLASSPATH:%{_javadir}/smtp.jar
CLASSPATH=$CLASSPATH:%{_javadir}/jython.jar
CLASSPATH=$CLASSPATH:%{_javadir}/commons-logging.jar
CLASSPATH=$CLASSPATH:%{_javadir}/xml-commons-apis.jar
CLASSPATH=$CLASSPATH:%{_javadir}/bcel.jar
CLASSPATH=$CLASSPATH:%{_javadir}/jsse.jar
CLASSPATH=$CLASSPATH:%{_javadir}/jce.jar
CLASSPATH=$CLASSPATH:%{_javadir}/log4j.jar
CLASSPATH=$CLASSPATH:%{_javadir}/junit.jar
CLASSPATH=$CLASSPATH:%{_javadir}/jaxp_transform_impl.jar

#ln -sf %{_javalibdir}/commons-logging.jar lib/
#ln -sf %{_javalibdir}/mail.jar lib/
#ln -sf %{_javalibdir}/activation.jar lib/
#ln -sf %{_javalibdir}/jython.jar lib/
#ln -sf %{_javalibdir}/log4j.jar lib/
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-jmx-module.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-mx4j-module.jar

cd build
ant jars javadocs docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}
cp dist/lib/%{name}-actions.jar $RPM_BUILD_ROOT%{_javadir}
cp dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}
cp dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}-actions.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-actions-%{version}.jar
ln -sf %{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-jmx-%{version}.jar
ln -sf %{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tools-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc dist/docs
%{_javadir}/*.jar
