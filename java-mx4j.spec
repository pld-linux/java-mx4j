#
# Conditional build:
%bcond_with	doc	# build docs (broken)
#
# TODO:
#		- update to 2.0.1
#
Summary:	Open source implementation of JMX Java API
Summary(pl):	Implementacja API Javy JMX z otwartymi ¼ród³ami
Name:		mx4j
Version:	1.1.1
Release:	0.2
Epoch:		0
License:	Apache License
Group:		Development/Languages/Java
# File http://dl.sf.net/%{name}/%{name}-%{version}.tar.gz have unusable sources!
# So, we'll use a snap from jpp (probably a cvs snapshot).
Source0:	%{name}-%{version}jpp.tar.gz
# Source0-md5:	ec2413473675f67a17e9819d78343d84
URL:		http://mx4j.sourceforge.net/
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	jaf
BuildRequires:	jakarta-bcel >= 5.0
BuildRequires:	jakarta-commons-logging >= 1.0.1
BuildRequires:	jakarta-log4j >= 1.2.7
BuildRequires:	javamail >= 1.2
BuildRequires:	jce >= 1.2.2
BuildRequires:	jpackage-utils
BuildRequires:	jsse >= 1.0.2
BuildRequires:	junit >= 3.8
BuildRequires:	jython >= 2.1
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xml-commons
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

%package doc
Summary:	Manual for %{name}
Summary(fr):	Documentation pour %{name}
Summary(it):	Documentazione di %{name}
Summary(pl):	Podrêcznik dla %{name}a
Group:		Development/Languages/Java

%description doc
Documentation for %{name}.

%description doc -l fr
Documentation pour %{name}.

%description doc -l it
Documentazione di %{name}.

%description doc -l pl
Dokumentacja do %{name}a.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name} -

%description javadoc -l pl
Dokumentacja do %{name}a -

%prep
%setup -q -n %{name}
find lib -type f ! -name "xdoclet*.jar" ! -name "docbook*.*" ! -name "xjavadoc*.jar" -exec rm -f {} ';'

%build
export JAVA_HOME="%{java_home}"

required_jars="\
activation \
mailapi.jar \
javamail/smtp \
jython \
commons-logging \
xml-commons-apis \
bcel \
jsse \
jce \
log4j \
junit \
jaxp_transform_impl \
"

export CLASSPATH=$(/usr/bin/build-classpath $required_jars)

#ln -sf %{_javalibdir}/commons-logging.jar lib/
#ln -sf %{_javalibdir}/mail.jar lib/
#ln -sf %{_javalibdir}/activation.jar lib/
#ln -sf %{_javalibdir}/jython.jar lib/
#ln -sf %{_javalibdir}/log4j.jar lib/
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-jmx-module.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-mx4j-module.jar

cd build
%ant jars %{?with_docs:javadocs docs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp dist/lib/%{name}-actions.jar $RPM_BUILD_ROOT%{_javadir}
cp dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}
cp dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{name}-actions.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-actions-%{version}.jar
ln -sf %{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-jmx-%{version}.jar
ln -sf %{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tools-%{version}.jar

# javadoc
%if %{with doc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with doc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%endif
